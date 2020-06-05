#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <opencv2/imgproc/types_c.h>

using namespace std;
using namespace cv;

void isSkinArea(Mat ycrcb[], Mat& Skin_img) {
	Skin_img = Mat(ycrcb[0].rows, ycrcb[0].cols, CV_8U);
	for (int i = 0; i < ycrcb[0].rows; i++) {
		for (int j = 0; j < ycrcb[0].cols; j++) {
			if (ycrcb[0].at<uchar>(i, j) > 80 &&
				ycrcb[1].at<uchar>(i, j) > 135 && ycrcb[1].at<uchar>(i, j) < 180 &&
				ycrcb[2].at<uchar>(i, j) > 85 && ycrcb[2].at<uchar>(i, j) < 135)
				Skin_img.at<uchar>(i, j) = 255;
			else
				Skin_img.at<uchar>(i, j) = 0;
		}
	}
}

int main() {

	Mat BGR_img = imread("C:\\Users\\yul\\Desktop\\상율\\과제\\3-1\\영상처리 및 실습\\예림.jpg");
	Mat HSV_img, bgr[3], ycrcb[3], Skin_img, Skin_img_color;

	cvtColor(BGR_img, HSV_img, CV_BGR2YCrCb);

	split(HSV_img, ycrcb);
	split(BGR_img, bgr);

	isSkinArea(ycrcb, Skin_img);


	Matx <uchar, 3, 3> mask;
	mask << 0, 1, 0,
		1, 1, 1,
		0, 1, 0;

	//morphologyEx(Skin_img, Skin_img, MORPH_OPEN, mask);
	//morphologyEx(Skin_img, Skin_img, MORPH_CLOSE, mask);


	bgr[0] = bgr[0].mul((Skin_img / 255));
	bgr[1] = bgr[1].mul((Skin_img / 255));
	bgr[2] = bgr[2].mul((Skin_img / 255));

	merge(bgr, 3, Skin_img_color);


	imshow("Original", BGR_img);
	imshow("Montage", Skin_img);


	waitKey(0);

	return 0;

}
