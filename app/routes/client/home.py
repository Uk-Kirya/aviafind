import uuid

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.responses import JSONResponse, Response
from app.core.limiter import limiter

from app.redis import redis_client
from app.settings import templates, settings

home = APIRouter(
    include_in_schema=True,
    tags=["Главная страница"]
)


@home.get(
    path="/",
    response_class=HTMLResponse,
    name="home",
    summary="Главная страница"
)
async def home_page(
        request: Request,
) -> HTMLResponse or RedirectResponse:
    """
    Главная страница
    :param request: Request object
    :return: HTMLResponse
    """

    return templates.TemplateResponse(
        "client/home.html",
        {
            "request": request,
        },
    )


@home.get(
    path="/policy",
    response_class=HTMLResponse,
    name="policy",
    summary="Политика конфиденциальности"
)
async def home_page(
        request: Request,
) -> HTMLResponse or RedirectResponse:
    """
    Политика конфиденциальности
    :param request: Request object
    :return: HTMLResponse
    """

    return templates.TemplateResponse(
        "client/policy.html",
        {
            "request": request,
        },
    )


@home.post(
    path="/agreed-to-policy",
    summary="Соглашение с политикой конфиденциальности"
)
@limiter.limit("5/minute")
async def agreed(
        request: Request,
        response: Response
) -> JSONResponse:
    """
    Соглашение с политикой конфиденциальности
    :param request: Request object
    :param response: Response object
    :return: JSONResponse
    """

    session_id = str(uuid.uuid4())
    await redis_client.set(f"agreed:{session_id}", "True", ex=settings.SESSION_TTL)

    response = JSONResponse({"status": "ok"})
    response.set_cookie(
        "agreed", session_id, max_age=settings.SESSION_TTL, httponly=True
    )

    return response
