from dependency_injector import containers, providers
from CaptchaRecognition.captcha_recognizer import CaptchaRecognizer
from NcyuControllers.login_controller import LoginEndpoint
from NcyuControllers.grade_controller import GradeController
from NcyuControllers.course_selection_controller import CourseSelectionController
from NcyuControllers.personal_course_controller import CourseEndpoint
from Proxies.ncyu_proxy import NcyuAPIProxy

class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            "NcyuControllers.login_controller",
            "NcyuControllers.grade_controller",
            "NcyuControllers.personal_course_controller",
            "Proxies.ncyu_proxy",
        ]
    )

    config = providers.Configuration()

    captcha_recognizer = providers.Singleton(
        CaptchaRecognizer,
    )

    ncyu_api_proxy = providers.Factory(
        NcyuAPIProxy,
        captcha_recognizer=captcha_recognizer,
    )

    login_controller = providers.Factory(
        LoginEndpoint,
        ncyu_api_proxy=ncyu_api_proxy,
    )

    grade_controller = providers.Factory(
        GradeController,
        ncyu_api_proxy=ncyu_api_proxy,
    )

    course_selection_controller = providers.Factory(
        CourseSelectionController,
    )

    course_controller = providers.Factory(
        CourseEndpoint,
        ncyu_api_proxy=ncyu_api_proxy,
    )
