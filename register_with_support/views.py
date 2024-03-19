import logging
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import Lower
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    FormView,
    View,
)
from pyexpat import ExpatError
from xmlschema import XMLSchemaException

from .forms import *
from .metadata_builder.metadata_structures import *
from .metadata_builder.utils import *

from common import models
from common.decorators import login_session_institution_required
from resource_management.views import (
    _INDEX_PAGE_TITLE,
    _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
    _create_manage_resource_page_title
)
from user_management.services import (
    get_user_id_for_login_session,
    get_institution_id_for_login_session,
)
from validation.file_wrappers import XMLMetadataFile
from validation.services import MetadataFileXSDValidator


logger = logging.getLogger(__name__)


# Create your views here.

@method_decorator(login_session_institution_required, name='dispatch')
class ResourceRegisterWithoutFileFormView(FormView):
    success_url = ''
    form_class = None
    template_name = ''

    model = None
    metadata_builder_class = None
    file_upload_registration_url = ''
    resource_management_list_page_breadcrumb_url_name = ''
    resource_management_list_page_breadcrumb_text = ''

    institution_id = None
    owner_id = None

    def process_form(self, form_cleaned_data):
        # Make copy of cleaned data
        processed_form = form_cleaned_data
        processed_form['localid'] = f'{self.model.localid_base}_{processed_form["localid"]}'
        processed_form['namespace'] = processed_form["namespace"]
        return processed_form

    def register_xml_file(self, request, xml_file, name):
        self.model.objects.create_from_xml_string(
            xml_file.read(),
            self.institution_id,
            self.owner_id,
        )
        messages.success(request, f'Successfully registered {name}.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in kwargs:
            context['form'] = self.get_form()
        context['success_url'] = self.success_url
        context['localid_base'] = self.model.localid_base
        context['title'] = f'New {self.model.type_readable.title()}'
        context['organisation_short_names'] = {o.metadata_server_url: o.short_name for o in models.Organisation.objects.all()}
        context['localid_validation_url'] = reverse_lazy('validation:new_localid')
        context['resource_management_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_text'] = _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:data_collection_related_metadata_index'
        context['resource_management_list_page_breadcrumb_text'] = self.resource_management_list_page_breadcrumb_text
        context['resource_management_list_page_breadcrumb_url_name'] = self.resource_management_list_page_breadcrumb_url_name
        return context

    def form_valid(self, form):
        processed_form = self.process_form(form.cleaned_data)
        metadata_builder = self.metadata_builder_class(processed_form)
        xml = metadata_builder.xml
        localid = processed_form['localid']
        name = processed_form['name']
        xml_file = SimpleUploadedFile(f'{localid}.xml', xml.encode('utf-8'))
        try:
            MetadataFileXSDValidator.validate(XMLMetadataFile.from_file(xml_file))
        except XMLSchemaException as err:
            logger.exception('Generated XML failed schema validation.')
            form_error_msg = f'''
            This form was unable to be processed into schema-valid XML due to the translation
            code becoming outdated with the metadata schema.
            <br><br>
            Whilst this functionality is unavailable, the <a href="{self.file_upload_registration_url}">file upload functionality</a> can be used
            as an alternative to register your metadata. Please also consider <a href="{reverse_lazy('support')}" target="_blank">
            notifying our support team</a> about this problem.
            <br><br>
            We apologise for any inconvenience caused.
            '''
            messages.error(self.request, form_error_msg)
            return self.render_to_response(self.get_context_data(form=form))
        except BaseException as err:
            logger.exception('An unexpected error occurred whilst running XSD validation on generated XML.')
            form_error_msg = f'''
            An unexpected error occurred whilst validating the generated XML against the schema.
            Please try submitting the form again, or if the issue persists, <a href="{reverse_lazy('support')}" target="_blank">
            let our support team know</a>.
            '''
            messages.error(self.request, form_error_msg)
            return self.render_to_response(self.get_context_data(form=form))
        
        try:
            xml_file.seek(0)
            self.register_xml_file(self.request, xml_file, name)
        except ExpatError as err:
            logger.exception('Expat error occurred during registration process.')
            messages.error(self.request, f'There was a problem during XML generation. Please report this error to our support team.')
            return self.render_to_response(self.get_context_data(form=form))
        except IntegrityError as err:
            logger.exception('The local ID submitted is already in use.')
            messages.error(self.request, 'The local ID submitted is already in use.')
            return self.render_to_response(self.get_context_data(form=form))
        except BaseException as err:
            logger.exception('An unexpected error occurred during registration.')
            messages.error(self.request, 'An unexpected error occurred during registration.')
            return self.render_to_response(self.get_context_data(form=form))
        
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'The form submitted was not valid.')
        return super().form_invalid(form)
    
    def dispatch(self, request, *args, **kwargs):
        self.institution_id = get_institution_id_for_login_session(request.session)
        self.owner_id = get_user_id_for_login_session(request.session)
        return super().dispatch(request, *args, **kwargs)

class OrganisationSelectFormViewMixin(View):
    def get_organisation_choices_for_form(self):
        return (
            ('', ''),
            *[(o.metadata_server_url, o.name) for o in models.Organisation.objects.annotate(json_name=KeyTextTransform('name', 'json')).all().order_by(Lower('json_name'))],
        )

class RelatedPartiesSelectFormViewMixin(View):
    def get_related_party_choices_for_form(self):
        return (
            ('', ''),
            ('Organisations', (
                (o.metadata_server_url, o.name) for o in models.Organisation.objects.annotate(json_name=KeyTextTransform('name', 'json')).all().order_by(Lower('json_name'))
            )),
            ('Individuals', (
                (o.metadata_server_url, o.name) for o in models.Individual.objects.annotate(json_name=KeyTextTransform('name', 'json')).all().order_by(Lower('json_name'))
            ))
        )

class OrganisationRegisterWithoutFileFormView(ResourceRegisterWithoutFileFormView):
    success_url = reverse_lazy('register:organisation_no_file')
    form_class = OrganisationInputSupportForm
    template_name = 'register_with_support/organisation_form.html'

    model = models.Organisation
    metadata_builder_class = OrganisationMetadata
    file_upload_registration_url = reverse_lazy('register:organisation')

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('organisations')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:organisations'

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)

        processed_form['namespace'] = 'pithia'

        # Hours of service
        hours_of_service = process_hours_of_service_in_form(form_cleaned_data)
        processed_form['hours_of_service'] = hours_of_service
        
        # Contact info
        processed_form['contact_info'] = process_contact_info_in_form(form_cleaned_data)

        return processed_form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'namespace': 'pithia'}
        return kwargs

class IndividualRegisterWithoutFileFormView(OrganisationSelectFormViewMixin, ResourceRegisterWithoutFileFormView):
    success_url = reverse_lazy('register:individual_no_file')
    form_class = IndividualInputSupportForm
    template_name = 'register_with_support/individual_form.html'

    model = models.Individual
    metadata_builder_class = IndividualMetadata
    file_upload_registration_url = reverse_lazy('register:individual')

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('individuals')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:individuals'

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)

        # Hours of service
        hours_of_service = process_hours_of_service_in_form(form_cleaned_data)
        processed_form['hours_of_service'] = hours_of_service
        
        # Contact info
        processed_form['contact_info'] = process_contact_info_in_form(form_cleaned_data)

        return processed_form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organisation_choices'] = self.get_organisation_choices_for_form()
        return kwargs

class ProjectRegisterWithoutFileFormView(
    OrganisationSelectFormViewMixin,
    RelatedPartiesSelectFormViewMixin,
    ResourceRegisterWithoutFileFormView):
    success_url = reverse_lazy('register:project_no_file')
    form_class = ProjectInputSupportForm
    template_name = 'register_with_support/project_form.html'

    model = models.Project
    metadata_builder_class = ProjectMetadata
    file_upload_registration_url = reverse_lazy('register_project')

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Project.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:projects'

    def get_status_choices_for_form():
        pass

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)

        return processed_form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organisation_choices'] = self.get_organisation_choices_for_form()
        kwargs['related_party_choices'] = self.get_related_party_choices_for_form()
        return kwargs