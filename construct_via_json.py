import json

class LabelJsonEncoder:

	def __init__(self, project_name):
		self.main_body = {}

		# attributes
		_via_attributes = {}
		_via_attributes['region'] = {}
		_via_attributes['file'] = {}
		self.main_body['_via_attributes'] = _via_attributes

		# settings
		_via_settings = {}
		ui = {}
		ui['annotation_editor_height'] = 25
		ui['annotation_editor_fontsize'] = 0.8
		ui['leftsidebar_width'] = 18
		image_grid = {}
		image_grid['img_height'] = 80
		image_grid['rshape_fill'] = 'none'
		image_grid['rshape_fill_opacity'] = 0.3
		image_grid['rshape_stroke'] = 'yellow'
		image_grid['rshape_stroke_width'] = 2
		image_grid['show_region_shape'] = True
		image_grid['show_image_policy'] = 'all'
		ui['image_grid'] = image_grid
		image = {}
		image['region_label'] = '__via_region_id__'
		image['region_label_font'] = '10px Sans'
		image['on_image_annotation_editor_placement'] = 'NEAR_REGION'
		ui['image'] = image
		_via_settings['ui'] = ui

		core = {}
		core['buffer_size'] = 18
		core['filepath'] = {}
		core['default_filepath'] = './files/'
		_via_settings['core'] = core
		project = {}
		project['name'] = project_name
		_via_settings['project'] = project
		self.main_body['_via_settings'] = _via_settings
		# img data
		self._via_img_metadata = {}


	def add_label_set(self, filename, img_size, bboxes):
		data = {}
		data['file_attributes'] = {}
		data['filename'] = filename
		data['size'] = img_size
		data['regions'] = []
		for box in bboxes:
			region = {}
			region['region_attributes'] = {}
			shape_attributes = {}
			shape_attributes['name'] = 'rect'
			shape_attributes['x'] = int(box[1])
			shape_attributes['y'] = int(box[0])
			shape_attributes['width'] = int(box[3] - box[1])
			shape_attributes['height'] = int(box[2] - box[0])
			region['shape_attributes'] = shape_attributes
			data['regions'].append(region)

		self._via_img_metadata[filename] = data


	def commit(self):
		self.main_body['_via_img_metadata'] = self._via_img_metadata
		with open('tmp.json', 'w') as outfile:
			outfile.write(json.dumps(self.main_body))


if __name__ == '__main__':
	filename = '2019-10-01 14_34_03.411508.jpg'
	new_instance = LabelJsonEncoder('test') # give project name
	new_instance.add_label_set(filename, 373956, [[100, 100, 200, 200]])
	new_instance.commit()
