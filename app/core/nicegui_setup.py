"""NiceGUI integration with FastAPI"""
from fastapi import FastAPI
from nicegui import ui

def setup_nicegui(app: FastAPI):
    """Setup NiceGUI integration with FastAPI"""
    # Mount NiceGUI with FastAPI
    ui.run_with(app, mount_path="/", storage_secret="subway-surfers-secret")