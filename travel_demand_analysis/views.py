from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
import json
from django.utils.safestring import mark_safe
import os
import pygeoj
import geojson
import os.path, time
from .custom_models.constants import *
from .custom_models.FourStepModel import TripGeneration, TripDistribution, ModalSplit
from .custom_models.TravelAnalyzing import TripAnalyzer
import pandas as pd


def travel_analysis(request):
    amenity_directory = "media/amenities"
    household_directory = "media/households"
    trafficzone_directory = "media/trafficzones"
    landuse_directory = "media/landuses"
    if not os.path.exists(amenity_directory):
        print("MAKE DIR1")
        os.makedirs(amenity_directory)
    if not os.path.exists(landuse_directory):
        print("MAKE DIR1")
        os.makedirs(landuse_directory)
    if not os.path.exists(household_directory):
        print("MAKE DIR2")
        os.makedirs(household_directory)
    if not os.path.exists(trafficzone_directory):
        print("MAKE DIR3")
        os.makedirs(trafficzone_directory)


    amenity_filenames = [file for file in os.listdir(amenity_directory) if file.endswith('_cleaned.geojson')]
    household_filenames = os.listdir(household_directory)
    trafficzone_filenames = os.listdir(trafficzone_directory)
    landuse_filenames = os.listdir(landuse_directory)
    print("FILES: "+str(household_filenames)+":"+str(amenity_filenames)+":"+str(trafficzone_filenames))

    with open('travel_demand_analysis/coors.json', encoding='utf8') as f:
        json_data = json.load(f)

    return render(request, 'Analysis.html', {
        'coordinates_var': json_data["features"],
        'amenity_filenames': amenity_filenames,
        'household_filenames': household_filenames,
        'trafficzone_filenames': trafficzone_filenames,
        'landuse_filenames': landuse_filenames
    })


def run_analysis(request):
    if request.is_ajax() and request.POST:
        amenity_files = request.POST.getlist('amenity_files[]')
        household_files = request.POST.getlist('household_files[]')
        trafficzone_files = request.POST.getlist('trafficzone_files[]')
        landuse_files = request.POST.getlist('landuse_files[]')
        trip_analyzer = TripAnalyzer(trafficzone_files, household_files, amenity_files, landuse_files)
        preprocessed_frame, taz_info_preanalysis = trip_analyzer.trip_analyze()
        preprocessed_frame.to_csv("media/PRE_TRIPGEN_FINISHED.csv", encoding='utf-8')
        trip_generation = TripGeneration("media/PRE_TRIPGEN_FINISHED.csv", "trips")

        trip_generation.setProductionParameters(production_attribute_names,
                                                production_attribute_intercept,
                                                production_attribute_coeffiients)
        trip_generation.setAttractionParameters(attraction_attribute_names,
                                                attraction_attribute_intercept,
                                                attraction_attribute_coeffiients)

        df, overall_trip_production, overall_trip_attraction = trip_generation.printAllZonalTripsProductionAttraction()
#
        salary = [
            (28914.53774)/30.0*8,
            (15272.45278)/30.0*8,
            (18041.69932)/30.0*8,
            (15941.61762)/30.0*8,
            (18043.87723)/30.0*8,
            (31188.91655)/30.0*8,
            (17686.01605)/30.0*8,
            (18341.81337)/30.0*8,
            (19328.20344)/30.0*8,
            (31416.64932)/30.0*8,
            (29100.03951)/30.0*8,
            (29338.63793)/30.0*8,
            (34532.08523)/30.0*8,
            (29759.84905)/30.0*8,
            (59292.40187)/30.0*8,
            (23177.36298)/30.0*8,
            (31113.8259)/30.0*8
        ]

        fareJeep = [[22.89, 16.44, 17.72, 21.94, 26.11, 26.14, 18.31, 29.61, 27.59, 43.42, 47.42, 44.56, 48.98, 46.24, 45.68, 45.62, 46.49], [17.69, 14.57, 14.52, 18.16, 22.82, 23.08, 16.93, 26.71, 28.11, 41.21, 45.66, 42.28, 46.41, 41.8, 41.77, 42.68, 41.56], [18.55, 14.18, 12.75, 17.22, 19.41, 19.47, 11.59, 22.92, 25.76, 45.05, 49.31, 46.02, 49.91, 45.63, 44.66, 44.52, 45.24], [22.41, 17.37, 17.43, 10.37, 15.07, 15.27, 18.7, 20.38, 22.11, 47.23, 50.08, 45.91, 49.3, 44.92, 44.66, 45.86, 43.72], [26.51, 22.3, 19.64, 15.23, 8.5, 9.09, 18.52, 12.88, 14.67, 43.79, 46.21, 40.82, 44.5, 39.71, 38.87, 40.55, 38.07], [26.46, 22.85, 19.55, 15.66, 9.04, 9.63, 17.29, 12.32, 13.3, 45.2, 49.39, 44.87, 48.6, 43.92, 43.12, 45.32, 42.57], [18.64, 16.73, 11.33, 18.6, 18.49, 17.28, 11.18, 22.01, 22.14, 46.69, 50.19, 46.9, 50.62, 48.04, 46.79, 47.0, 47.91], [30.22, 27.2, 24.85, 20.69, 13.08, 12.75, 22.08, 14.44, 12.82, 49.62, 53.04, 48.45, 52.1, 47.32, 47.52, 49.57, 46.33], [28.14, 27.58, 26.04, 21.73, 12.94, 12.94, 21.85, 13.2, 33.33, 48.61, 54.32, 49.13, 53.24, 48.16, 47.91, 50.5, 46.84], [41.26, 41.38, 43.56, 45.9, 46.18, 46.18, 43.47, 49.5, 51.96, 8.5, 14.38, 8.5, 17.0, 12.8, 10.35, 9.92, 16.85], [44.96, 43.69, 46.63, 47.1, 43.76, 46.22, 47.21, 50.61, 51.97, 13.3, 9.03, 8.78, 13.73, 14.52, 10.44, 9.54, 12.16], [42.23, 40.64, 43.95, 43.66, 39.52, 42.38, 44.97, 46.81, 47.76, 8.5, 9.6, 8.5, 10.79, 11.62, 8.5, 8.5, 9.02], [46.95, 44.46, 46.86, 46.58, 41.9, 45.21, 48.45, 49.87, 51.0, 17.0, 13.45, 10.15, 12.22, 15.35, 10.15, 12.51, 9.45], [44.12, 39.94, 43.45, 42.37, 37.12, 40.18, 45.43, 44.73, 45.16, 12.12, 14.73, 11.51, 15.53, 11.33, 11.86, 15.06, 11.93], [43.06, 40.5, 43.67, 42.8, 39.09, 41.83, 45.46, 46.22, 47.26, 10.39, 10.73, 8.5, 9.37, 11.94, 8.5, 10.07, 10.05], [43.66, 42.25, 43.76, 44.08, 40.56, 43.43, 45.02, 48.67, 48.0, 10.93, 10.07, 8.85, 13.11, 14.33, 9.79, 8.5, 10.62], [45.32, 39.6, 43.46, 41.73, 37.05, 39.97, 46.25, 44.67, 45.1, 16.92, 12.55, 9.16, 9.75, 12.18, 8.55, 11.63, 8.5]]
        fareBus = [[12.0, 12.0, 15.43, 20.02, 27.31, 30.54, 25.09, 35.67, 35.04, 68.12, 68.12, 68.12, 69.88, 75.19, 68.38, 68.12, 80.62], [12.0, 12.0, 13.71, 19.36, 24.0, 27.13, 23.5, 32.32, 31.59, 63.5, 63.5, 63.5, 65.25, 70.56, 63.75, 63.5, 76.0], [15.2, 14.57, 15.0, 20.83, 27.32, 30.65, 25.48, 35.59, 34.69, 67.0, 67.0, 67.0, 68.75, 74.06, 67.25, 67.0, 79.5], [20.08, 18.95, 20.3, 24.64, 17.37, 18.4, 22.91, 21.28, 19.9, 63.67, 63.67, 63.67, 65.42, 70.73, 63.92, 63.67, 76.17], [27.28, 24.0, 27.27, 17.54, 12.0, 12.0, 25.05, 12.53, 12.31, 62.25, 62.25, 62.25, 64.0, 69.31, 62.5, 62.25, 74.75], [30.83, 27.46, 30.87, 17.89, 12.0, 12.0, 26.5, 12.0, 12.0, 68.56, 68.56, 68.56, 70.31, 75.62, 68.81, 68.56, 81.06], [18.99, 18.2, 22.72, 19.71, 22.47, 27.12, 30.19, 30.42, 30.0, 68.25, 68.21, 68.23, 69.7, 75.28, 68.7, 68.25, 80.75], [36.08, 32.62, 35.98, 18.88, 12.82, 12.0, 27.83, 12.0, 12.0, 73.62, 73.62, 73.62, 75.38, 80.69, 73.88, 73.62, 86.12], [35.75, 32.07, 35.43, 18.69, 12.34, 12.0, 23.6, 12.0, 0, 73.25, 73.25, 73.25, 75.0, 80.31, 73.5, 73.25, 85.75], [60.41, 54.88, 60.75, 54.78, 53.25, 59.52, 61.35, 64.38, 63.75, 12.0, 12.0, 12.0, 12.0, 16.03, 12.0, 12.0, 21.25], [60.44, 55.5, 59.06, 55.38, 53.88, 60.12, 60.25, 65.0, 64.38, 12.0, 12.0, 12.0, 12.0, 15.16, 12.0, 12.0, 19.81], [56.29, 51.38, 54.92, 51.25, 49.75, 56.0, 56.11, 60.88, 60.25, 51.5, 37.88, 12.0, 39.56, 13.02, 12.0, 12.0, 15.67], [52.5, 47.62, 51.12, 47.5, 46.0, 52.25, 52.33, 57.12, 56.5, 62.25, 62.25, 62.25, 0, 12.0, 62.25, 62.25, 12.12], [47.69, 42.81, 46.31, 42.69, 41.19, 47.44, 47.52, 52.31, 51.69, 57.44, 57.44, 51.85, 46.38, 25.52, 55.55, 51.25, 12.0], [53.5, 48.62, 52.12, 48.5, 47.0, 53.25, 53.33, 58.12, 57.5, 63.25, 63.25, 63.25, 0, 12.0, 12.0, 0, 12.88], [55.12, 50.12, 53.75, 50.0, 48.5, 54.75, 54.92, 59.62, 59.0, 64.75, 47.17, 64.75, 12.0, 12.5, 0, 0, 14.5], [44.38, 39.62, 43.0, 39.5, 38.0, 44.25, 44.25, 49.12, 48.5, 54.25, 54.25, 54.25, 56.0, 48.3, 54.5, 54.25, 12.0]]
        travelTimeJeep = [[1.3009, 1.0177, 0.9718, 0.9958, 1.2149, 1.1023, 0.9036, 1.4169, 1.2598, 2.1136, 2.2729, 2.1788, 2.3402, 2.1537, 2.1397, 2.1464, 2.1394], [1.0897, 0.9561, 0.8134, 0.8023, 1.0249, 0.9274, 0.8474, 1.2433, 1.2692, 2.0517, 2.2268, 2.0554, 2.2451, 1.8603, 1.94, 2.0164, 1.868], [1.0131, 0.7824, 0.5161, 0.7052, 1.023, 0.7758, 0.5695, 1.1476, 1.1321, 2.2472, 2.4338, 2.2766, 2.4552, 2.1058, 2.1005, 2.1476, 2.0912], [1.0023, 0.7933, 0.7242, 0.3804, 0.7368, 0.6001, 0.6734, 0.9623, 0.9645, 2.1901, 2.3336, 2.1773, 2.3345, 1.9627, 2.0004, 2.1276, 1.9404], [1.2202, 1.0123, 1.0194, 0.7508, 0.4537, 0.5264, 0.814, 0.8575, 0.8766, 2.2865, 2.3782, 2.2014, 2.3351, 1.9676, 1.9768, 2.0989, 1.9512], [1.1248, 0.9373, 0.7629, 0.6114, 0.521, 0.3286, 0.5708, 0.6994, 0.6205, 2.3122, 2.4465, 2.2901, 2.4948, 2.1217, 2.1613, 2.2328, 2.0965], [0.9244, 0.8412, 0.5605, 0.669, 0.8009, 0.5753, 0.4792, 0.9592, 0.9084, 2.3354, 2.4189, 2.3198, 2.4596, 2.1958, 2.1889, 2.2265, 2.1919], [1.4472, 1.2836, 1.2265, 0.9808, 0.8679, 0.6816, 0.9607, 0.8168, 0.6296, 2.6198, 2.7111, 2.5736, 2.7641, 2.3991, 2.4035, 2.493, 2.3638], [1.302, 1.2659, 1.1812, 0.9937, 0.8639, 0.6205, 0.9072, 0.697, 1.5476, 2.5467, 2.6901, 2.5602, 2.7468, 2.3695, 2.432, 2.4632, 2.327], [2.0722, 2.0054, 2.1876, 2.1624, 2.1871, 2.2739, 2.2476, 2.5662, 2.5598, 0.2413, 0.4577, 0.4225, 0.58, 0.7103, 0.5149, 0.448, 0.7553], [2.2499, 2.1617, 2.3546, 2.2276, 2.2171, 2.3646, 2.3628, 2.6542, 2.6763, 0.4736, 0.3928, 0.4633, 0.5244, 0.6934, 0.547, 0.4821, 0.7499], [2.167, 2.0497, 2.2491, 2.0881, 2.071, 2.2232, 2.2682, 2.4941, 2.4892, 0.4253, 0.4547, 0.3383, 0.4609, 0.5152, 0.3632, 0.3499, 0.6092], [2.3199, 2.1905, 2.3657, 2.2292, 2.197, 2.3775, 2.3943, 2.6562, 2.6614, 0.561, 0.5049, 0.4792, 0.4931, 0.6689, 0.5614, 0.5257, 0.7502], [2.1526, 1.8489, 2.1111, 1.8926, 1.8523, 2.0356, 2.1392, 2.3119, 2.3232, 0.6995, 0.6955, 0.5, 0.6874, 0.345, 0.3639, 0.4178, 0.409], [2.1521, 1.9427, 2.1681, 1.9666, 1.8929, 2.082, 2.195, 2.3667, 2.3476, 0.5108, 0.571, 0.3484, 0.5414, 0.3762, 0.2136, 0.2875, 0.4256], [2.1309, 1.9436, 2.14, 1.9551, 1.9009, 2.0876, 2.1728, 2.4389, 2.3804, 0.4528, 0.4764, 0.3481, 0.531, 0.4421, 0.3139, 0.2056, 0.4563], [2.1732, 1.8477, 2.0912, 1.8477, 1.8048, 1.9925, 2.1106, 2.2669, 2.2672, 0.7554, 0.7761, 0.6083, 0.7648, 0.4164, 0.4222, 0.4823, 0.4012]]
        travelTimeBus = [[0.4814, 0.5313, 0.5438, 1.0047, 1.2155, 1.3968, 0.9851, 1.6134, 1.559, 2.4794, 2.5282, 2.6776, 3.0697, 3.0052, 2.8733, 2.8078, 3.3101], [0.5337, 0.4147, 0.5066, 0.9145, 1.0612, 1.2558, 0.9682, 1.4324, 1.4412, 2.2871, 2.3358, 2.4852, 2.8774, 2.8128, 2.681, 2.6154, 3.1178], [0.5349, 0.5123, 0.5135, 0.9647, 1.1949, 1.3614, 0.9176, 1.5788, 1.5415, 2.4546, 2.5033, 2.6527, 3.0449, 2.9803, 2.8485, 2.7829, 3.2853], [1.0046, 0.866, 0.9434, 1.0531, 0.7498, 0.7903, 1.0088, 1.0177, 0.9429, 2.3766, 2.4253, 2.5747, 2.9669, 2.9023, 2.7705, 2.7049, 3.2073], [1.2207, 1.0474, 1.2076, 0.7606, 0.4444, 0.5129, 1.0815, 0.7429, 0.6885, 2.2556, 2.3043, 2.4537, 2.8458, 2.7813, 2.6494, 2.5839, 3.0862], [1.4302, 1.2258, 1.3629, 0.7696, 0.5239, 0.2374, 1.0991, 0.4153, 0.3613, 2.4116, 2.4603, 2.6097, 3.0019, 2.9374, 2.8055, 2.7399, 3.2423], [0.8538, 0.8665, 0.9758, 0.999, 1.0539, 1.129, 1.283, 1.2893, 1.2349, 2.5391, 2.5717, 2.715, 3.0898, 3.0767, 2.9358, 2.8844, 3.4261], [1.6291, 1.4315, 1.5927, 0.9666, 0.7614, 0.4219, 1.2879, 0.3199, 0.301, 2.641, 2.6897, 2.8391, 3.2313, 3.1667, 3.0349, 2.9693, 3.4717], [1.6336, 1.3797, 1.539, 0.9549, 0.7, 0.3979, 1.1153, 0.3008, 0, 2.5875, 2.6363, 2.7856, 3.1778, 3.1133, 2.9814, 2.9158, 3.4182], [2.6895, 2.4743, 2.6854, 2.5598, 2.4242, 2.5908, 2.752, 2.805, 2.7506, 0.2631, 0.2681, 0.4175, 0.8096, 0.7451, 0.6132, 0.5476, 1.05], [2.7081, 2.509, 2.6715, 2.5935, 2.457, 2.6234, 2.7732, 2.8381, 2.7837, 0.5394, 0.2308, 0.358, 0.7501, 0.6856, 0.5538, 0.4882, 0.9906], [2.5532, 2.3542, 2.5167, 2.4386, 2.3022, 2.4685, 2.6183, 2.6832, 2.6289, 2.0065, 1.5681, 0.406, 1.7094, 0.5155, 0.4198, 0.4512, 0.8357], [2.6635, 2.4644, 2.6269, 2.5489, 2.4124, 2.5788, 2.7286, 2.7935, 2.7392, 2.6444, 2.6932, 2.7822, 0, 0.641, 3.0258, 2.9728, 0.946], [2.1955, 1.9965, 2.159, 2.0809, 1.9444, 2.1108, 2.2606, 2.3255, 2.2712, 2.1765, 2.2252, 2.1229, 2.1883, 1.0111, 2.4812, 2.2602, 0.478], [2.6193, 2.4203, 2.5828, 2.5047, 2.3683, 2.5347, 2.6844, 2.7493, 2.695, 2.6003, 2.649, 2.7667, 0, 0.5969, 0.5133, 0, 0.9039], [2.7293, 2.5303, 2.6928, 2.6147, 2.4783, 2.6447, 2.7944, 2.8593, 2.805, 2.7103, 2.0063, 2.7869, 0.7714, 0.7069, 0, 0, 1.0118], [2.0614, 1.8624, 2.0249, 1.9468, 1.8103, 1.9767, 2.1265, 2.1914, 2.1371, 2.0424, 2.0911, 2.2405, 2.6326, 2.0401, 2.4299, 2.3707, 0.3961]]
        fare = [[17.45, 14.22, 16.57, 20.98, 26.71, 28.34, 21.7, 32.64, 31.31, 55.77, 57.77, 56.34, 59.43, 60.72, 57.03, 56.87, 63.56], [14.85, 13.29, 14.12, 18.76, 23.41, 25.1, 20.21, 29.52, 29.85, 52.36, 54.58, 52.89, 55.83, 56.18, 52.76, 53.09, 58.78], [16.88, 14.38, 13.88, 19.02, 23.37, 25.06, 18.54, 29.26, 30.23, 56.02, 58.16, 56.51, 59.33, 59.84, 55.95, 55.76, 62.37], [21.24, 18.16, 18.87, 17.5, 16.22, 16.84, 20.8, 20.83, 21.0, 55.45, 56.88, 54.79, 57.36, 57.83, 54.29, 54.77, 59.95], [26.9, 23.15, 23.45, 16.38, 10.25, 10.54, 21.79, 12.71, 13.49, 53.02, 54.23, 51.53, 54.25, 54.51, 50.69, 51.4, 56.41], [28.64, 25.16, 25.21, 16.77, 10.52, 10.82, 21.89, 12.16, 12.65, 56.88, 58.98, 56.72, 59.45, 59.77, 55.97, 56.94, 61.81], [18.81, 17.46, 17.02, 19.16, 20.48, 22.2, 20.69, 26.22, 26.07, 57.47, 59.2, 57.56, 60.16, 61.66, 57.75, 57.62, 64.33], [33.15, 29.91, 30.41, 19.79, 12.95, 12.38, 24.95, 13.22, 12.41, 61.62, 63.33, 61.04, 63.74, 64.0, 60.7, 61.59, 66.22], [31.95, 29.82, 30.73, 20.21, 12.64, 12.47, 22.73, 12.6, 33.33, 60.93, 63.78, 61.19, 64.12, 64.23, 60.7, 61.88, 66.3], [50.83, 48.13, 52.16, 50.34, 49.72, 52.85, 52.41, 56.94, 57.86, 10.25, 13.19, 10.25, 14.5, 14.42, 11.18, 10.96, 19.05], [52.7, 49.59, 52.84, 51.24, 48.82, 53.17, 53.73, 57.8, 58.17, 12.65, 10.52, 10.39, 12.87, 14.84, 11.22, 10.77, 15.98], [49.26, 46.01, 49.44, 47.45, 44.64, 49.19, 50.54, 53.84, 54.0, 30.0, 23.74, 10.25, 25.18, 12.32, 10.25, 10.25, 12.34], [49.73, 46.04, 48.99, 47.04, 43.95, 48.73, 50.39, 53.49, 53.75, 39.62, 37.85, 36.2, 12.22, 13.68, 36.2, 37.38, 10.79], [45.91, 41.38, 44.88, 42.53, 39.16, 43.81, 46.48, 48.52, 48.42, 34.78, 36.09, 31.68, 30.96, 18.43, 33.7, 33.16, 11.96], [48.28, 44.56, 47.89, 45.65, 43.05, 47.54, 49.39, 52.17, 52.38, 36.82, 36.99, 35.88, 9.37, 11.97, 10.25, 10.07, 11.46], [49.39, 46.19, 48.75, 47.04, 44.53, 49.09, 49.97, 54.14, 53.5, 37.84, 28.62, 36.8, 12.55, 13.41, 9.79, 8.5, 12.56], [44.85, 39.61, 43.23, 40.61, 37.52, 42.11, 45.25, 46.89, 46.8, 35.59, 33.4, 31.7, 32.88, 30.24, 31.52, 32.94, 10.25]]
        travelTime = [[0.8911, 0.7745, 0.7578, 1.0002, 1.2152, 1.2496, 0.9444, 1.5151, 1.4094, 2.2965, 2.4005, 2.4282, 2.705, 2.5795, 2.5065, 2.4771, 2.7248], [0.8117, 0.6854, 0.66, 0.8584, 1.0431, 1.0916, 0.9078, 1.3378, 1.3552, 2.1694, 2.2813, 2.2703, 2.5613, 2.3365, 2.3105, 2.3159, 2.4929], [0.774, 0.6473, 0.5148, 0.835, 1.109, 1.0686, 0.7435, 1.3632, 1.3368, 2.3509, 2.4686, 2.4646, 2.75, 2.5431, 2.4745, 2.4653, 2.6883], [1.0034, 0.8296, 0.8338, 0.7167, 0.7433, 0.6952, 0.8411, 0.99, 0.9537, 2.2833, 2.3795, 2.376, 2.6507, 2.4325, 2.3855, 2.4162, 2.5739], [1.2205, 1.0299, 1.1135, 0.7557, 0.4491, 0.5196, 0.9477, 0.8002, 0.7826, 2.271, 2.3413, 2.3276, 2.5905, 2.3744, 2.3131, 2.3414, 2.5187], [1.2775, 1.0816, 1.0629, 0.6905, 0.5225, 0.283, 0.8349, 0.5574, 0.4909, 2.3619, 2.4534, 2.4499, 2.7484, 2.5295, 2.4834, 2.4863, 2.6694], [0.8891, 0.8538, 0.7681, 0.834, 0.9274, 0.8521, 0.8811, 1.1242, 1.0716, 2.4372, 2.4953, 2.5174, 2.7747, 2.6363, 2.5623, 2.5554, 2.809], [1.5381, 1.3576, 1.4096, 0.9737, 0.8146, 0.5517, 1.1243, 0.5684, 0.4653, 2.6304, 2.7004, 2.7064, 2.9977, 2.7829, 2.7192, 2.7311, 2.9177], [1.4678, 1.3228, 1.3601, 0.9743, 0.7819, 0.5092, 1.0112, 0.4989, 1.5476, 2.5671, 2.6632, 2.6729, 2.9623, 2.7414, 2.7067, 2.6895, 2.8726], [2.3808, 2.2398, 2.4365, 2.3611, 2.3056, 2.4324, 2.4998, 2.6856, 2.6552, 0.2522, 0.3629, 0.42, 0.6948, 0.7277, 0.564, 0.4978, 0.9026], [2.479, 2.3354, 2.513, 2.4105, 2.337, 2.494, 2.568, 2.7462, 2.73, 0.5065, 0.3118, 0.4106, 0.6372, 0.6895, 0.5504, 0.4851, 0.8702], [2.3601, 2.202, 2.3829, 2.2633, 2.1866, 2.3458, 2.4432, 2.5886, 2.5591, 1.2159, 1.0114, 0.3721, 1.0852, 0.5153, 0.3915, 0.4005, 0.7225], [2.4917, 2.3274, 2.4963, 2.3891, 2.3047, 2.4782, 2.5614, 2.7248, 2.7003, 1.6027, 1.5991, 1.6307, 0.4931, 0.655, 1.7936, 1.7492, 0.8481], [2.1741, 1.9227, 2.135, 1.9868, 1.8983, 2.0732, 2.1999, 2.3187, 2.2972, 1.438, 1.4604, 1.3115, 1.4379, 0.6781, 1.4225, 1.339, 0.4435], [2.3857, 2.1815, 2.3754, 2.2357, 2.1306, 2.3083, 2.4397, 2.558, 2.5213, 1.5555, 1.61, 1.5575, 0.5414, 0.4865, 0.3634, 0.2875, 0.6647], [2.4301, 2.237, 2.4164, 2.2849, 2.1896, 2.3662, 2.4836, 2.6491, 2.5927, 1.5816, 1.2413, 1.5675, 0.6512, 0.5745, 0.3139, 0.2056, 0.734], [2.1173, 1.855, 2.0581, 1.8973, 1.8075, 1.9846, 2.1185, 2.2291, 2.2022, 1.3989, 1.4336, 1.4244, 1.6987, 1.2282, 1.4261, 1.4265, 0.3987]]

        faresModes = [fareJeep, fareBus]
        travelTimesModes = [travelTimeJeep, travelTimeBus]

        td = TripDistribution(overall_trip_production, overall_trip_attraction, travelTime, fare, salary)
        #distribution = td.getTripDistribution()
        distribution = td.getDummyOD(len(overall_trip_production), len(overall_trip_production))
        flattened_distrib = [val for sublist in distribution for val in sublist]
        pandas_distrib = pd.DataFrame(distribution, columns=range(0, len(overall_trip_production)))
        #zonal_od_matrix = json.dumps(distribution, indent=4)
        #print(" od_matrix: "+str(zonal_od_matrix))

        modal_split = ModalSplit(distribution, "datapath", salary, faresModes, travelTimesModes)
        list_of_dataframes_by_mode = modal_split.process_od_matrix()
        for index, list in enumerate(list_of_dataframes_by_mode):
            pandas_modsplit = pd.DataFrame(list, columns=range(0, len(overall_trip_production)))
            pandas_modsplit.to_csv("media/SAMPLE_ZONAL_modsplit"+str(index)+".csv", encoding='utf-8')

        for index, zone_info in enumerate(taz_info_preanalysis):
            zone_info.trips_produced = round(overall_trip_production[index], 2)
            zone_info.trips_attracted = round(overall_trip_attraction[index], 2)

        flattened_distrib_jeep = [val for sublist in list_of_dataframes_by_mode[0] for val in sublist]
        flattened_distrib_bus = [val for sublist in list_of_dataframes_by_mode[1] for val in sublist]

        zone_info_json = json.dumps([ob.__dict__ for ob in taz_info_preanalysis], default=lambda o: o.__dict__,
                                    indent=4, sort_keys=True)
        pandas_distrib.to_csv("media/SAMPLE_ZONAL_ODODODOD.csv", encoding='utf-8')
        df.to_csv("media/SAMPLE_ZONAL_PROD_ATTR.csv", encoding='utf-8')
        data = {}
        data['max_trip_produced'] = max(overall_trip_production)
        data['max_trip_attracted'] = max(overall_trip_attraction)
        data['taz_json'] = zone_info_json
        data['zonal_od'] = distribution
        data['zonal_od_jeep'] = list_of_dataframes_by_mode[0]
        data['zonal_od_bus'] = list_of_dataframes_by_mode[1]
        data['max_distrib'] = max(flattened_distrib)
        data['max_distrib_jeep'] = max(flattened_distrib_jeep)
        data['max_distrib_bus'] = max(flattened_distrib_bus)

        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("Non ajax post request")


def analysis_add_amenity(request):
    if request.is_ajax() and request.POST:
        amenity_filename = request.POST.get('amenity_filename')
        file_path = "media/amenities/" + str(amenity_filename)

        with open(file_path, encoding="utf-8") as f:
            json_data = json.load(f)
        amenity_dump = json.dumps(json_data)

        data = {}
        data['no_amenities'] = len(json_data['features'])
        data['amenity_filename'] = amenity_filename
        data['amenities_json'] = amenity_dump


        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("Non ajax post request")

def analysis_add_household(request):
    if request.is_ajax() and request.POST:
        household_filename = request.POST.get('household_filename')
        file_path = "media/households/" + str(household_filename)

        with open(file_path, encoding="utf-8") as f:
            json_data = json.load(f)
        household_dump = json.dumps(json_data)
        data = {}
        data['no_households'] = len(json_data)
        data['household_filename'] = household_filename
        data['households_json'] = household_dump
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("Non ajax post request")


def analysis_add_trafficzone(request):
    if request.is_ajax() and request.POST:
        trafficzone_filename = request.POST.get('trafficzone_filename')
        file_path = "media/trafficzones/" + str(trafficzone_filename)

        geofile = pygeoj.load(file_path)
        zone_tally = 0
        for feature in geofile:
            zone_tally = zone_tally + 1

        data = {}
        data['no_trafficzones'] = zone_tally
        data['trafficzone_filename'] = trafficzone_filename
        data['zone_geojson'] = geojson.dumps(geofile)
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("Non ajax post request")

def analysis_add_landuse(request):
    if request.is_ajax() and request.POST:
        landuse_filename = request.POST.get('landuse_filename')
        file_path = "media/landuses/" + str(landuse_filename)


        with open(file_path, encoding="utf-8") as f:
            json_data = json.load(f)
        landuse_dump = json.dumps(json_data)



        data = {}
        data['no_landuses'] = len(json_data['features'])
        data['landuse_filename'] = landuse_filename
        data['landuses_json'] = landuse_dump
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("Non ajax post request")
