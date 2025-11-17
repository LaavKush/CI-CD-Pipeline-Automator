from fastapi import APIRouter
router = APIRouter(prefix='/apply-fix')

@router.post('/')
def apply_fix():
    return {'msg':'apply fix placeholder'}
