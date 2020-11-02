from run_model import modelRunner

modelRunner = modelRunner('trained_model/frozen_inference_graph.pb')
out_dict = modelRunner.run_inference('data/example_images/image00006.jpg')

print(out_dict) # {'total': 4, 'empty': 3, 'occupied': 1}