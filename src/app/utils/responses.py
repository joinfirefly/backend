from typing import Optional

from robyn import Response

def Redirect(location: str, status_code: int = 302, headers: Optional[dict] = None, description: Optional[str] = None) -> Response:
    """
    Function to create a Response instance for HTTP redirects.

    @param location: The URL to redirect to.
    @param status_code: The status code of the redirect response.
    @param headers: Additional headers for the response.
    @param description: The description of the response.
    @return: A Response instance configured for redirection.
    """
    if headers is None:
        headers = {}
    headers["Location"] = location
    return Response(
        status_code=status_code,
        headers=headers,
        description=description if description else f"Redirecting to {location}",
        response_type="text/html"
    )

def XMLResponse(xml_body: str, status_code: int = 200, headers: Optional[dict] = None) -> Response:
    """
    Function to create a Response instance for XML responses.

    @param xml_body: The XML content of the response.
    @param status_code: The status code of the XML response.
    @param headers: Additional headers for the response.
    @return: A Response instance configured for XML content.
    """
    if headers is None:
        headers = {}
    headers["Content-Type"] = "application/xml"
    return Response(
        status_code=status_code,
        headers=headers,
        description=xml_body,
        response_type="application/xml"
    )