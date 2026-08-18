from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='app/templates')
router = APIRouter()

@router.get('/reg', response_class=HTMLResponse, tags=['users'])
async def get_reg(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='reg.html'
    )

@router.get('/log', response_class=HTMLResponse, tags=['users'])
async def get_log(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='log.html'
    )

