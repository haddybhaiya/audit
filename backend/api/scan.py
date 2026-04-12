from fastapi import APIRouter
from backend.data_layer.dataset_loader import load_dataset
from backend.data_layer.proxy_scanner import (
    scan_name_proxies,
    scan_correlation_proxies,
)
from backend.data_layer.balance_checker import check_balance

router = APIRouter(prefix="/scan", tags=["scan"])

@router.get('/')
def scan_dataset(filename:str, protected:str):
    df = load_dataset(filename)
    name_proxies = scan_name_proxies(df)
    corr_proxies = scan_correlation_proxies(df, protected)
    balance = check_balance(df, protected)
    return {
        "name_proxies": name_proxies,
        "correlation_proxies": corr_proxies,
        "balance": balance 
    }