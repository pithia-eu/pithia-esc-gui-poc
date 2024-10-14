const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
const COPY_BUTTON_TOOLTIP_DEFAULT_TEXT = 'Copy to clipboard';
const COPY_BUTTON_TOOLTIP_COPIED_TEXT = 'Copied!';

async function copyMemberEmailAddress(memberEmailAddress) {
    await navigator.clipboard.writeText(memberEmailAddress);
}

window.addEventListener("load", async () => {
    const dropdowns = document.querySelectorAll(".dropdown-institution-member");
    for await (const dropdown of dropdowns) {
        // Copy email button - add event listener
        const copyEmailAddressButton = dropdown.querySelector(".btn-copy-email-address");
        const emailAddress = dropdown.querySelector("input").value;
        const tooltip = bootstrap.Tooltip.getInstance(copyEmailAddressButton);
        copyEmailAddressButton.addEventListener("click", async () => {
            await copyMemberEmailAddress(emailAddress);
            tooltip.setContent({
                '.tooltip-inner': COPY_BUTTON_TOOLTIP_COPIED_TEXT
            });
        });
        copyEmailAddressButton.addEventListener("hide.bs.tooltip", () => {
            tooltip.setContent({
                '.tooltip-inner': COPY_BUTTON_TOOLTIP_DEFAULT_TEXT
            });
        });
    }
});