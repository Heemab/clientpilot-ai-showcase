from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict):
    """
    Render a Django template as a PDF.

    Returns:
        HttpResponse containing the PDF,
        or None if PDF generation fails.
    """

    template = get_template(template_src)
    html = template.render(context_dict)

    result = BytesIO()

    pdf = pisa.pisaDocument(
        src=BytesIO(html.encode("UTF-8")),
        dest=result,
        encoding="UTF-8",
    )

    if pdf.err:
        return None

    response = HttpResponse(
        result.getvalue(),
        content_type="application/pdf",
    )

    return response