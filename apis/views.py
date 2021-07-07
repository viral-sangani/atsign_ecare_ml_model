from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apis.ml_model import get_prediction_MNIST


@api_view(["POST"])
def getResponse(request):
    if request.method == "POST":
        if request.data.get("file", None) == None:
            return Response(
                {"error": "File not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        file = request.data["file"]
        print(file)
        print("Hello World")
        img_bytes = file.read()
        return Response({"Hi": "111"})
        # dict = get_prediction_MNIST(image_bytes=img_bytes)
        # item = {}
        # for i in dict:
        #     item[i] = str(dict[i])
        # return Response(
        #     {
        #         "data": {
        #             "COVID19": item[0],
        #             "Lung Opacity": item[1],
        #             "Normal": item[2],
        #             "Viral Pneumonia": item[3],
        #             "Atelectasis": item[4],
        #             "Consolidation": item[5],
        #             "Infiltration": item[6],
        #             "Pneumothorax": item[7],
        #             "Edema": item[8],
        #             "Emphysema": item[9],
        #             "Fibrosis": item[10],
        #             "Effusion": item[11],
        #         }
        #     },
        #     status=status.HTTP_200_OK,
        # )
