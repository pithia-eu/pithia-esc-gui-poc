export function enableHandleInfoPopover() {
    const handleInfoPopoverTrigger = document.querySelector('#handle-info-popover');
    const handleInfoPopover = new bootstrap.Popover(
        handleInfoPopoverTrigger,
        {
            content: `
            <p>
                Handles are identifiers for digital objects
                and other resources in distributed computer systems.
            </p>
            For more information, visit these articles:
            <ul class="mb-0">
                <li>
                    <a href="https://www.dona.net/handle-system" target="_blank" class="link-underline-by-default">
                    The Handle System</a>
                </li>
                <li>
                    <a href="http://www.cnri.reston.va.us/home/cstr/handle-overview.html" target="_blank" class="link-underline-by-default">
                    The Handle System: A Technical Overview</a>
                </li>
            </ul>
            `,
            html: true,
            trigger: "focus",
        }
    );
}

window.addEventListener("load", () => {
    enableHandleInfoPopover();
});