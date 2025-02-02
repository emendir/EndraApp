if __package__ is None: # if this script is executed directly not as part of a package 
    import os ,sys
    os.system(f"{sys.executable} {os.path.dirname(os.path.dirname(__file__))}")
else:
    from .main import run_app
    run_app()