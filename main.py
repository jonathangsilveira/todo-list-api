

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app="src.app:app",
        host="0.0.0.0",
        port=8000,
        log_config="log_config.yaml",
        reload=True
    )