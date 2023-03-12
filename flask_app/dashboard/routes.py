# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, request, url_for, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound


from flask_app.dashboard import blueprint
from flask_app.dashboard.forms import RetryForm, UploadForm, FailurePipelineForm, MainPipelineForm, ProcessorsForm
from logic.controller.construct_graph_controler import ConstructGraphControler
from logic.pipeline.dynamic_pipeline.dynamic_pipeline import DynamicPipeline
from logic.pipeline.main_pipeline.main_pipeline import MainPipeline
from logic.pipeline.failure_pipeline.failure_pipeline import FailurePipeline
from logic.controller.search_controler import SearchControler
from utility.logger import Logger 
from connector.neo4j_helper import Neo4jHelper
from configuration.configs import Configs

@blueprint.route("/health-check")
def health_check():
    return 'healthy', 200

def costumSerializable(sub_graph):
    #Since we can't serialize neo2py Relationship objects, we implement a custom serializable here
    simple_obj = []
    for item in sub_graph:
        nodes = item['nodes']
        relationships = item['relationships']
        paths = item['paths']
        simple_paths = []
        for path in paths:
            simple_path = {}
            simple_path['score'] = path['score']
            simple_path['path'] = []
            for rel in path['path']:
                simple_rel = {}
                simple_rel['label'] = rel.__class__.__name__
                simple_rel['start_node'] = rel.start_node
                simple_rel['end_node'] = rel.end_node
                simple_path['path'].append(simple_rel)
            simple_paths.append(simple_path)
        simple_relationships = []
        for rel in relationships:
            simple_rel = {}
            simple_rel['label'] = rel.__class__.__name__
            simple_rel['start_node'] = rel.start_node
            simple_rel['end_node'] = rel.end_node
            simple_relationships.append(simple_rel)
        simple_obj.append({'nodes': nodes, 'relationships': simple_relationships, 'paths': simple_paths})
    return simple_obj

@blueprint.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    hop = request.args.get('hop')
    if query and hop:
        result = SearchControler().search(query, hop)
        return jsonify(result=costumSerializable(result))
    else:
        return "missed user query, add the query param in this way: ?query='the query string'&hop=int"

@blueprint.route('/test', methods=['GET'])
def test():
    neo4j_helper = Neo4jHelper(Configs.neo4j_url, Configs.neo4j_user, Configs.neo4j_pass)
    data = neo4j_helper.find_one_node(address='test')
    return jsonify({'message': f'Received data: {data}'})
    
@blueprint.route('/submit', methods=['POST'])
def submit():
    data = request.json
    return jsonify({'message': f'Received data: {data}'})


@blueprint.route('/pipelines/start', methods=['POST'])
@login_required
def run_upload_pipeline():
    pipelines = {
        'MainPipeline': {
            'class': MainPipeline
        },
        'FailurePipeline': {
            'class': FailurePipeline
        },
        'DynamicPipeline': {
            'class': DynamicPipeline
        }
    }
    data = request.get_json()
    controller = ConstructGraphControler()
    pipeline_class = pipelines[data['pipeline']]['class']
    data.pop('pipeline')
    controller.run_pipeline_local(MainPipeline)
    return {'result': 'ok'}


@blueprint.route('/processors/start', methods=['POST'])
@login_required
def run_processors():
    data = request.get_json()
    #extract txs_ids and selected_processors from the input box
    txs_ids = None
    if 'listings' in data and data['listings'] and data['listings'] != '':
        txs_ids_str = data['listings']
        data.pop('listings')
        txs_ids = txs_ids_str.split(',')
    controller = ConstructGraphControler()
    controller.run_pipeline_local(DynamicPipeline, txs_ids=txs_ids, **data)
    return {'result': 'ok'}


@blueprint.route('/pipelines/stop/<string:pipeline>', methods=['POST'])
@login_required
def stop_upload_pipeline(pipeline):
    controller = ConstructGraphControler()
    # controller.stop()
    return {'result': 'ok'}


@blueprint.route('/pipelines/run-failed/<string:process>', methods=['POST'])
@login_required
def run_failed_pipeline(process):
    data = request.get_json()
    limit = None
    if 'limit' in data and data['limit'] != '':
        limit = int(data['limit'])
    controller = ConstructGraphControler()
    # if process == 'image':
    #     controller.run_pipeline(controller.run_failed_images_pipeline, limit)
    # else:
    #     controller.run_pipeline(controller.run_failed_pipelines)
    return {'result': 'ok'}


@blueprint.route('/index')
@login_required
def index():
    failure_form = FailurePipelineForm(request.form)
    main_form = MainPipelineForm(request.form)
    controller: ConstructGraphControler = ConstructGraphControler()
    return render_template('index.html', segment='index',
                           tabs=[
                               {
                                   'name': 'MainPipeline',
                                   'title': 'Main pipeline',
                                   'inProgress': False,
                                   'remaining_count': 0,
                                   'form': main_form,
                                   'href': url_for('dashboard_blueprint.run_upload_pipeline'),
                                   'stop_href': url_for('dashboard_blueprint.stop_upload_pipeline', pipeline='upload')
                               },
                               {
                                   'name': 'FailurePipeline',
                                   'title': 'Failure pipeline',
                                   'inProgress': True,
                                   'remaining_count': 0,
                                   'form': failure_form,
                                   'href': url_for('dashboard_blueprint.run_upload_pipeline'),
                                   'stop_href': url_for('dashboard_blueprint.stop_upload_pipeline', pipeline='upload')
                               },
                           ])


@blueprint.route('/processors')
@login_required
def processors():
    processors = ['NodeProcessor',
                  'EdgeProcessor',
                  'EdgeInterpreter',
                  'GraphInsertor'
                  ]
    processor_form = ProcessorsForm(request.form)
    processor_form.processors.choices = [(p, p) for p in processors]
    return render_template('processors.html', segment='processors',
                           processors=processors,
                           href=url_for('dashboard_blueprint.run_processors'),
                           form=processor_form
                           )


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template(template, segment=segment)

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
