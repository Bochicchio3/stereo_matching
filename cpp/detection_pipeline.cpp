// License: Apache 2.0. See LICENSE file in root directory.
// Copyright(c) 2017 Intel Corporation. All Rights Reserved.
// License: Apache 2.0. See LICENSE file in root directory.
// Copyright(c) 2017 Intel Corporation. All Rights Reserved.

#include <librealsense2/rs.hpp> // Include RealSense Cross Platform API
#include <opencv2/opencv.hpp>   // Include OpenCV API

int main(int argc, char * argv[]) try
{
    // Declare depth colorizer for pretty visualization of depth data
    rs2::colorizer color_map;

    rs2::config cfg;

    cfg.enable_all_streams();

    cfg.disable_stream(RS2_STREAM_ACCEL);
    cfg.disable_stream(RS2_STREAM_GYRO);
    // Declare RealSense pipeline, encapsulating the actual device and sensors
    rs2::pipeline pipe;
    // Start streaming with default recommended configuration
    pipe.start(cfg);

    using namespace cv;

    const auto window_name = "Display Infrared Left Image";
    const auto window_name = "Display Infrared Right Image";
    
    const auto window_name = "Display Depth Image";
    const auto window_name = "Display Color Image";
    
    namedWindow(window_name, WINDOW_AUTOSIZE);
    int b;
    b=waitKey(1);

    double a;
    a=getWindowProperty(window_name, WND_PROP_AUTOSIZE);

    while (waitKey(1)!=113 && getWindowProperty(window_name, WND_PROP_AUTOSIZE) >= 0)
    {
        rs2::frameset data = pipe.wait_for_frames();   // Wait for next set of frames from the camera
        //                         // Print each enabled stream frame rate
        rs2::frame depth = data.get_depth_frame().apply_filter(color_map);
        // // rs2::frame color = data.get_color_frame();
        // // rs2::frame fisheye = data.get_fisheye_frame();
        rs2::frame infrared = data.get_infrared_frame();

        // // Query frame size (width and height)
        const int w = depth.as<rs2::video_frame>().get_width();
        const int h = depth.as<rs2::video_frame>().get_height();
        // break;

        // // Create OpenCV matrix of size (w,h) from the colorized depth data
        // // Mat image(Size(w, h), CV_8UC3, (void*)depth.get_data(), Mat::AUTO_STEP);
        Mat image2(Size(w,h), CV_8UC3, (void*)infrared.get_data(), Mat::AUTO_STEP);
        // // Mat image3(Size(w,h), CV_8UC3, (void*)fisheye.get_data(), Mat::AUTO_STEP);
        // // Mat image4(Size(w,h), CV_8UC3, (void*)infrared.get_data(), Mat::AUTO_STEP);
        // // Mat image2(Size(w,h), CV_8UC3, (void*)color.get_data(), Mat::AUTO_STEP);

        // // Update the window with new data
        imshow(window_name, image2);
        // imshow("a", image2);
        // imshow("b", image3);
        // imshow("c", image4);
        // imshow(window_name, image);
        
    }

    return EXIT_SUCCESS;
}
catch (const rs2::error & e)
{
    std::cerr << "RealSense error calling " << e.get_failed_function() << "(" << e.get_failed_args() << "):\n    " << e.what() << std::endl;
    return EXIT_FAILURE;
}
catch (const std::exception& e)
{
    std::cerr << e.what() << std::endl;
    return EXIT_FAILURE;
}


    // cfg.enable_stream(RS2_)
    // cfg.disable_stream(RS2_STREAM_ACCEL);
    // cfg.disable_stream(RS2_STREAM_GYRO);
    
    // rs2::log_to_console(RS2_LOG_SEVERITY_ERROR);
    // // Create a simple OpenGL window for rendering:
    // window app(1280, 720, "RealSense Capture Example");
    // std::cout<<"OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO";
    // // Declare depth colorizer for pretty visualization of depth data
    // rs2::colorizer color_map;
    // // Declare rates printer for showing streaming rates of the enabled streams.
    // rs2::rates_printer printer;

    // // Declare RealSense pipeline, encapsulating the actual device and sensorsa
    // rs2::pipeline pipe;

    // Start streaming with default recommended configuration
    // The default video configuration contains Depth and Color streams
    // If a device is capable to stream IMU data, both Gyro and Accelerometer are enabled by default
//     pipe.start(cfg);

//     while (app) // Application still alive?
//     {
//         rs2::frameset data = pipe.wait_for_frames().    // Wait for next set of frames from the camera
//                              apply_filter(printer).     // Print each enabled stream frame rate
//                              apply_filter(color_map);   // Find and colorize the depth data

//         // The show method, when applied on frameset, break it to frames and upload each frame into a gl textures
//         // Each texture is displayed on different viewport according to it's stream unique id
//         app.show(data);
//     }

//     return EXIT_SUCCESS;
// }
// catch (const rs2::error & e)
// {
//     std::cerr << "RealSense error calling " << e.get_failed_function() << "(" << e.get_failed_args() << "):\n    " << e.what() << std::endl;
//     return EXIT_FAILURE;
// }
// catch (const std::exception& e)
// {
//     std::cerr << e.what() << std::endl;
//     return EXIT_FAILURE;
// }


