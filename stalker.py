import pyzed.sl as sl

from data_processors import to_csv
import data_service


OBJECT_DETECTED_STARTING_FROM_PERCENT = 40
CONFIDENCE_THRESHOLD = 50
MAXIMUM_DISTANCE_IN_METERS = 30
MEASUREMENTS_PER_SECOND = 15
ACCURACY = 5


def initialize():
    zed = sl.Camera()

    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD1080
    init_params.camera_fps = MEASUREMENTS_PER_SECOND
    init_params.coordinate_units = sl.UNIT.METER
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP
    init_params.depth_mode = sl.DEPTH_MODE.ULTRA
    init_params.depth_maximum_distance = MAXIMUM_DISTANCE_IN_METERS

    return zed, init_params


def clean_up(zed):
    zed.disable_object_detection()
    zed.disable_positional_tracking()
    zed.close()


if __name__ == "__main__":
    zed, init_params = initialize()
    status = zed.open(init_params)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()

    # Enable positional tracking module
    positional_tracking_parameters = sl.PositionalTrackingParameters()

    # If the camera is static in space, enabling this setting below provides better depth quality and faster computation
    positional_tracking_parameters.set_as_static = True
    zed.enable_positional_tracking(positional_tracking_parameters)

    obj_param = sl.ObjectDetectionParameters()
    obj_param.detection_model = sl.DETECTION_MODEL.MULTI_CLASS_BOX_ACCURATE
    obj_param.enable_tracking = True
    zed.enable_object_detection(obj_param)

    obj_runtime_param = sl.ObjectDetectionRuntimeParameters()
    obj_runtime_param.detection_confidence_threshold = OBJECT_DETECTED_STARTING_FROM_PERCENT
    obj_runtime_param.object_class_filter = [sl.OBJECT_CLASS.PERSON]

    runtime_params = sl.RuntimeParameters()
    runtime_params.confidence_threshold = CONFIDENCE_THRESHOLD

    objects = sl.Objects()

    buffer_data = []
    # To use when the y_velocity from the camera is used
    detector_data = []
    old_detector_average = []

    while(1):
        if zed.grab(runtime_params) == sl.ERROR_CODE.SUCCESS:
            returned_state = zed.retrieve_objects(objects, obj_runtime_param)

            if (returned_state == sl.ERROR_CODE.SUCCESS and objects.is_new):
                obj_array = objects.object_list
                # To use when the y_velocity from the camera is wrong
                # buffer_data, old_detector_average = to_csv(obj_array, ACCURACY, MEASUREMENTS_PER_SECOND, buffer_data, old_detector_average)
                buffer_data, detector_data, old_detector_average = to_csv(obj_array, ACCURACY, MEASUREMENTS_PER_SECOND, buffer_data, detector_data, old_detector_average)
        data_service.main()

    clean_up(zed)
