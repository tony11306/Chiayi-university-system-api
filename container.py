import os
import json
from dotenv import load_dotenv

from dependency_injector import containers, providers
from firebase_admin import initialize_app, firestore, credentials
from CaptchaRecognition.captcha_recognizer import CaptchaRecognizer
from Proxies.ncyu_proxy import NcyuAPIProxy
from Proxies.firebase_proxy import FirebaseProxy

load_dotenv()

def _initialize_firebase_app():
    env_creds = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
    
    if not env_creds:
        raise RuntimeError(
            "Environment variable 'FIREBASE_SERVICE_ACCOUNT' not set. "
            "Please configure it in Cloud Run variables."
        )

    try:
        # 解析 JSON 字串並建立憑證
        cred_dict = json.loads(env_creds)
        cred = credentials.Certificate(cred_dict)
        return initialize_app(cred)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse 'FIREBASE_SERVICE_ACCOUNT' JSON: {e}")

class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            "NcyuControllers.login_controller",
            "NcyuControllers.grade_controller",
            "NcyuControllers.personal_course_controller",
            "NcyuControllers.course_selection_controller",
            "Proxies.ncyu_proxy",
            "Proxies.firebase_proxy",
        ]
    )

    config = providers.Configuration()

    # Firebase
    firebase_app = providers.Singleton(_initialize_firebase_app)
    db_client = providers.Singleton(
        firestore.client,
        app=firebase_app,
    )
    firebase_proxy = providers.Factory(
        FirebaseProxy,
        db=db_client,
    )

    # Captcha
    captcha_recognizer = providers.Singleton(
        CaptchaRecognizer,
    )

    # NCYU API
    ncyu_api_proxy = providers.Factory(
        NcyuAPIProxy,
        captcha_recognizer=captcha_recognizer,
    )

    # Controllers
    login_controller = providers.Factory(
        "NcyuControllers.login_controller.LoginEndpoint",
        ncyu_api_proxy=ncyu_api_proxy,
    )

    grade_controller = providers.Factory(
        "NcyuControllers.grade_controller.GradeController",
        ncyu_api_proxy=ncyu_api_proxy,
    )

    course_selection_controller = providers.Factory(
        "NcyuControllers.course_selection_controller.CourseSelectionController",
        firebase_proxy=firebase_proxy,
    )

    course_controller = providers.Factory(
        "NcyuControllers.personal_course_controller.CourseEndpoint",
        ncyu_api_proxy=ncyu_api_proxy,
    )
