#include <iostream>
#include <stdlib.h>
#include <ctime>

#include <opencv2/opencv.hpp>


using namespace std;

void draw_object(cv::Mat image, unsigned int x, unsigned int y, unsigned int width=50, unsigned int height=100)
{
    image(cv::Range(y-height, y), cv::Range(x-width/2, x+width/2)) = image.at<unsigned char>(y, x);
}


int main()
{
    unsigned int IMAGE_HEIGHT = 600;
    unsigned int IMAGE_WIDTH = 800;
    unsigned int MAX_DISP = 250;
    unsigned int CYCLE = 0;

    //setenv("QT_GRAPHICSSYSTEM", "native", 1);


    // === PREPERATIONS ==
    cv::Mat image = cv::Mat::zeros(IMAGE_HEIGHT, IMAGE_WIDTH, CV_8U);
    // cv::Mat uhist = cv::Mat::zeros(IMAGE_HEIGHT, MAX_DISP, CV_32F);
    // cv::Mat vhist = cv::Mat::zeros(MAX_DISP, IMAGE_WIDTH, CV_32F);

    cv::Mat uhist = cv::Mat::zeros(MAX_DISP, IMAGE_WIDTH, CV_32F);
    cv::Mat vhist = cv::Mat::zeros(IMAGE_WIDTH, MAX_DISP, CV_32F); 

    cv::Mat tmpImageMat, tmpHistMat;

    float value_ranges[] = {(float)0, (float)MAX_DISP};
    const float* hist_ranges[] = {value_ranges};
    int channels[] = {0};
    int histSize[] = {MAX_DISP};


    struct timespec start, finish;
    double elapsed;

    while(1)
    {
        CYCLE++;

        // === CLEANUP ==
        image = cv::Mat::zeros(IMAGE_HEIGHT, IMAGE_WIDTH, CV_8U);
        uhist = cv::Mat::zeros(IMAGE_HEIGHT, MAX_DISP, CV_32F);
        vhist = cv::Mat::zeros(MAX_DISP, IMAGE_WIDTH, CV_32F);

        // === CREATE FAKE DISPARITY WITH OBJECTS ===
        for(int i = 0; i < IMAGE_HEIGHT; i++)
            image.row(i) = ((float)i / IMAGE_HEIGHT * MAX_DISP);

        draw_object(image, 200, 500);
        draw_object(image, 525 + CYCLE%100, 275);
        draw_object(image, 500, 300 + CYCLE%100);

        clock_gettime(CLOCK_MONOTONIC, &start);

        // === CALCULATE V-HIST ===
        for(int i = 0; i < IMAGE_HEIGHT; i++)
        {
            tmpImageMat = image.row(i);
            vhist.row(i).copyTo(tmpHistMat);

            cv::calcHist(&tmpImageMat, 1, channels, cv::Mat(), tmpHistMat, 1, histSize, hist_ranges, true, false);

            vhist.row(i) = tmpHistMat.t() / (float) IMAGE_HEIGHT;
        }

        clock_gettime(CLOCK_MONOTONIC, &finish);
        elapsed = (finish.tv_sec - start.tv_sec);
        elapsed += (finish.tv_nsec - start.tv_nsec) * 1e-9;
        cout << "V-HIST-TIME: " << elapsed << endl;

        clock_gettime(CLOCK_MONOTONIC, &start);

        // === CALCULATE U-HIST ===
        image = image.t();
        for(int i = 0; i < IMAGE_WIDTH; i++)
        {
            tmpImageMat = image.row(i);
            uhist.col(i).copyTo(tmpHistMat);

            cv::calcHist(&tmpImageMat, 1, channels, cv::Mat(), tmpHistMat, 1, histSize, hist_ranges, true, false);

            uhist.col(i) = tmpHistMat / (float) IMAGE_WIDTH;
        }
        image = image.t();

        clock_gettime(CLOCK_MONOTONIC, &finish);
        elapsed = (finish.tv_sec - start.tv_sec);
        elapsed += (finish.tv_nsec - start.tv_nsec) * 1e-9;
        cout << "U-HIST-TIME: " << elapsed << endl;

        // === PREPARE AND SHOW RESULTS ===

        uhist.convertTo(uhist, CV_8U, 255);
        cv::applyColorMap(uhist, uhist, cv::COLORMAP_JET);

        vhist.convertTo(vhist, CV_8U, 255);
        cv::applyColorMap(vhist, vhist, cv::COLORMAP_JET);

        cv::imshow("image", image);
        cv::imshow("uhist", uhist);
        cv::imshow("vhist", vhist);



        if ((cv::waitKey(1)&255) == 'q')
            break;
    }

    return 0;
}   