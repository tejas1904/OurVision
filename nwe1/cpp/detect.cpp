#include <iostream>
#include <opencv2/opencv.hpp>

int main(int c, char **v) {
	Mat image = cv::imread("billboard.jpeg");
	if (image.empty()) {
		std::cout << "Could not load image!" << std::endl;
		return 0;
	} else {
		String window = "Image";
		cv::namedWindow(window);
		cv::imshow(window, image);
		cv::waitKey(0);
		cv::destroyWindow(window);
	}
	std::cout << "Hello, World!" << std::endl << std::endl;
	return 0;
}
