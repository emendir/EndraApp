
from endra_app.log import logger
import traceback


def main():
    try:
        from endra_app.entry_point import run
        run()
    except Exception as e:
        from crash_window import CrashWindow
        
        logger.error(traceback.format_exc()+ "\n" + str(e))

        error_message = (
            str(e)
             + "\n\n" + 
            '\n'.join(traceback.format_exc().split('\n')[-15:])
        )
        CrashWindow(error_message).run()


if __name__ == "__main__":
    main()
