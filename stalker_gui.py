import pyzed.sl as sl
import cv2
import numpy as np
import data_service

import cv_viewer.tracking_viewer as cv_viewer

from data_processors import to_csv

OBJECT_DETECTED_STARTING_FROM_PERCENT = 40
CONFIDENCE_THRESHOLD = 50
MAXIMUM_DISTANCE_IN_METERS = 30
MEASUREMENTS_PER_SECOND = 5
ACCURACY = 5

if __name__ == "__main__":
    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD1080
    init_params.coordinate_units = sl.UNIT.METER
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP
    init_params.depth_mode = sl.DEPTH_MODE.ULTRA
    init_params.depth_maximum_distance = MAXIMUM_DISTANCE_IN_METERS

    # Open the camera
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

    camera_infos = zed.get_camera_information()

    point_cloud_res = sl.Resolution(min(camera_infos.camera_resolution.width, 720), min(
        camera_infos.camera_resolution.height, 404))
    point_cloud_render = sl.Mat()

    # Configure object detection runtime parameters(len(sample_array)
    obj_runtime_param = sl.ObjectDetectionRuntimeParameters()
    obj_runtime_param.detection_confidence_threshold = OBJECT_DETECTED_STARTING_FROM_PERCENT
    # To select a set of specific object classes
    obj_runtime_param.object_class_filter = [sl.OBJECT_CLASS.PERSON]

    # Runtime parameters
    runtime_params = sl.RuntimeParameters()
    runtime_params.confidence_threshold = CONFIDENCE_THRESHOLD

    # Create objects that will store SDK outputs
    point_cloud = sl.Mat(point_cloud_res.width,
                         point_cloud_res.height, sl.MAT_TYPE.F32_C4, sl.MEM.CPU)
    objects = sl.Objects()
    image_left = sl.Mat()

    # Utilities for 2D display
    display_resolution = sl.Resolution(min(camera_infos.camera_resolution.width, 1280), min(
        camera_infos.camera_resolution.height, 720))
    image_scale = [display_resolution.width / camera_infos.camera_resolution.width,
                   display_resolution.height / camera_infos.camera_resolution.height]
    image_left_ocv = np.full((display_resolution.height, display_resolution.width, 4), [
                             245, 239, 239, 255], np.uint8)

    # Utilities for tracks view
    camera_config = zed.get_camera_information().camera_configuration
    tracks_resolution = sl.Resolution(400, display_resolution.height)
    track_view_generator = cv_viewer.TrackingViewer(
        tracks_resolution, camera_config.camera_fps, init_params.depth_maximum_distance)
    track_view_generator.set_camera_calibration(
        camera_config.calibration_parameters)
    image_track_ocv = np.zeros(
        (tracks_resolution.height, tracks_resolution.width, 4), np.uint8)

    # Will store the 2D image and tracklet views
    global_image = np.full((display_resolution.height, display_resolution.width +
                            tracks_resolution.width, 4), [245, 239, 239, 255], np.uint8)

    buffer_data = []
    detector_data = []
    old_detector_data = []

    while(1):
        if zed.grab(runtime_params) == sl.ERROR_CODE.SUCCESS:
            # Retrieve objects
            returned_state = zed.retrieve_objects(objects, obj_runtime_param)

            if (returned_state == sl.ERROR_CODE.SUCCESS and objects.is_new):
                # Retrieve point cloud
                zed.retrieve_measure(
                    point_cloud, sl.MEASURE.XYZRGBA, sl.MEM.CPU, point_cloud_res)
                point_cloud.copy_to(point_cloud_render)
                # Retrieve image
                zed.retrieve_image(image_left, sl.VIEW.LEFT,
                                   sl.MEM.CPU, display_resolution)
                image_render_left = image_left.get_data()
                # Get camera pose
                zed.get_position(sl.Pose(), sl.REFERENCE_FRAME.WORLD)

                update_render_view = True
                update_tracking_view = True

                # 2D rendering
                if update_render_view:
                    np.copyto(image_left_ocv, image_render_left)
                    cv_viewer.render_2D(
                        image_left_ocv, image_scale, objects, obj_param.enable_tracking)
                    global_image = cv2.hconcat(
                        [image_left_ocv, image_track_ocv])

                # Tracking view
                if update_tracking_view:
                    track_view_generator.generate_view(
                        objects, sl.Pose(), image_track_ocv, objects.is_tracked)

            cv2.imshow("ZED | 2D View and Birds View", global_image)
            cv2.waitKey(10)
            obj_array = objects.object_list
            for i in range(len(obj_array)):
                id = obj_array[i].id
                position = obj_array[i].position
                velocity = obj_array[i].velocity
                dimensions = obj_array[i].dimensions
                print(
                    f"ID: {id}\n3D position: [{position[0]},{position[1]},{position[2]}]\nVelocity: [{velocity[0]},{velocity[1]},{velocity[2]}]\n3D dimentions: [{dimensions[0]},{dimensions[1]},{dimensions[2]}]")
                buffer_data, detector_data, old_detector_data = to_csv(
                    obj_array, ACCURACY, MEASUREMENTS_PER_SECOND, buffer_data, detector_data, old_detector_data)
        data_service.main()

    cv2.destroyAllWindows()
    image_left.free(sl.MEM.CPU)
    point_cloud.free(sl.MEM.CPU)
    point_cloud_render.free(sl.MEM.CPU)

    # Disable modules and close camera
    zed.disable_object_detection()
    zed.disable_positional_tracking()

    zed.close()
