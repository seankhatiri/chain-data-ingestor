# from solidity_parser import parser
# import json
# import ast

# class ASTExtractor:

#     def __init__(self):
#         pass

#     def _node_to_code(self, node):
#         return None

#     def _comment_extractor(self):
#         comments = {}
#         for node in parser.walk(self.ast):
#             if isinstance(node, ast.FunctionDef):
#                 comment_list = ast.get_docstring(node)
#                 if comment_list:
#                     comments[node.name] = comment_list.strip()
#         return comments

#     def _func_finder(self, func_name):
#         for node in self.ast['children']:
#             if 'subNodes' in node:
#                 for sub_node in node['subNodes']:
#                     if node['type'] == 'ContractDefinition' and sub_node['type'] == 'FunctionDefinition' and sub_node['name'] == func_name:
#                         func_node = sub_node
#                         return func_node

#     def _functions_extractor(self, func_name):
#         # Find the function definition node for the setName function
#         internal_func_names = []
#         functions = {'main_func': {'node': '', 'code': ''}, 'internal_funcs': []}
#         func_node = self._func_finder(func_name)
#         functions['main_func']['node'], functions['main_func']['code'] = func_node, self._node_to_code(func_node)
#         for node in func_node['body']['statements']:
#             if node['type'] == 'ExpressionStatement' and node['expression']['type'] == 'FunctionCall':
#                 internal_func_names.append(node['expression']['expression']['name'])

#         for internal_func_name in internal_func_names:
#             functions['internal_funcs'].append({'node': self._func_finder(internal_func_name), 'code': self._node_to_code(self._func_finder(internal_func_name))})
#         return functions


#     def run(self, contract_code=None, func_name=None):
#         # get a smart contract code and the func that was called, then return a dict of main_func: main_func code, internall_func: [func1_code, func2_code]
#         self.ast = parser.parse(contract_code)
#         # print(json.dumps(self.ast, indent=4))
#         # print(json.dumps(self._functions_extractor(func_name), indent=4))
#         # print(self._functions_extractor(func_name))
#         print(self._comment_extractor())
#         return self._functions_extractor(func_name)

 
