#include "opencv2/opencv.hpp"

#include<iostream>
#include<stdio.h>
#include<math.h>

bool compare_contour_areas(std::vector<cv::Point> contour1, std::vector<cv::Point> contour2) {
	double area1 = fabs(cv::contourArea(cv::Mat(contour1)));
	double area2 = fabs(cv::contourArea(cv::Mat(contour2)));
	return area1 > area2;
}

bool compare_x(cv::Point point1, cv::Point point2) { return point1.x < point2.x; }

bool compare_y(cv::Point point1, cv::Point point2) { return point1.y < point2.y; }

bool compare_distance(std::pair<cv::Point, cv::Point> p1, std::pair<cv::Point, cv::Point> p2) {
	return norm(p1.first - p1.second) < norm(p2.first - p2.second);
}

double _distance(cv::Point p1, cv::Point p2) {
	return sqrt((p1.x-p2.x)*(p1.x-p2.x) + (p1.y-p2.y)*(p1.y-p2.y));
}

void resize_to_height(cv::Mat src, cv::Mat &dst, int height) {
	cv::Size size = cv::Size(src.cols * height / double(src.rows), height);
	cv::resize(src, dst, size, cv::INTER_AREA);
}

void order_points(std::vector<cv::Point> inputs, std::vector<cv::Point> &ordered) {
	sort(inputs.begin(), inputs.end(), compare_x);
	std::vector<cv::Point> lm(inputs.begin(), inputs.begin() + 2);
	std::vector<cv::Point> rm(inputs.end() - 2, inputs.end());
	
	sort(lm.begin(), lm.end(), compare_y);
	cv::Point tl(lm[0]);
	cv::Point bl(lm[1]);
	std::vector<std::pair<cv::Point, cv::Point>> tmp;
	
	for(size_t i = 0; i < rm.size(); i++) {
		tmp.push_back(std::make_pair(tl, rm[i]));
	}
	
	sort(tmp.begin(), tmp.end(), compare_distance);
	cv::Point tr(tmp[0].second);
	cv::Point br(tmp[0].second);
	
	ordered.push_back(tl);	
	ordered.push_back(tr);
	ordered.push_back(br);
	ordered.push_back(bl);
}

void four_point_transform(cv::Mat src, cv::Mat &dst, std::vector<cv::Point> points) {
	std::vector<cv::Point> ordered_points;
	order_points(points, ordered_points);
	
	double width_a = _distance(ordered_points[2], ordered_points[3]);
	double width_b = _distance(ordered_points[1], ordered_points[0]);
	double max_width = cv::max(width_a, width_b);
	
	double height_a = _distance(ordered_points[2], ordered_points[1]);
	double height_b = _distance(ordered_points[0], ordered_points[3]);
	double max_height = cv::max(height_a, height_b);
	
	cv::Point2f src_[] = {
		cv::Point2f(ordered_points[0].x, ordered_points[0].y),
		cv::Point2f(ordered_points[1].x, ordered_points[1].y),
		cv::Point2f(ordered_points[2].x, ordered_points[2].y),
		cv::Point2f(ordered_points[3].x, ordered_points[3].y)
	};
	cv::Point2f dst_[] = {
		cv::Point2f(0, 0),
		cv::Point2f(max_width-1, 0),
		cv::Point2f(max_width-1, max_height-1),
		cv::Point2f(0, max_height-1)
	};
	
	cv::Mat perspective_transform = cv::getPerspectiveTransform(src_, dst_);
	cv::warpPerspective(src, dst, perspective_transform, cv::Size(max_width, max_height));
}

int main() {
	cv::String imageName = "billboard.jpeg";
	cv::Mat image = cv::imread(imageName);
	if(image.empty()) {
		std::cout << "Couldn't load image or image not exists" << std::endl << std::endl;
		return 0;
	}
	cv::imwrite("Image.jpg", image);
}
