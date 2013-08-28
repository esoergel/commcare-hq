REPORT_CASE_INDEX="report_cases_1e249c9e4e85b3cbbd8e707b6e297d4d"
REPORT_CASE_MAPPING={'_meta': {'comment': 'Autogenerated [casexml.apps.case.models.CommCareCase] mapping from ptop_generate_mapping 08/22/2013',
           'created': None},
 'date_detection': False,
 'date_formats': ['yyyy-MM-dd',
                  "yyyy-MM-dd'T'HH:mm:ssZZ",
                  "yyyy-MM-dd'T'HH:mm:ss.SSSSSS",
                  "yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'",
                  "yyyy-MM-dd'T'HH:mm:ss'Z'",
                  "yyyy-MM-dd'T'HH:mm:ssZ",
                  "yyyy-MM-dd'T'HH:mm:ssZZ'Z'",
                  "yyyy-MM-dd'T'HH:mm:ss.SSSZZ",
                  "yyyy-MM-dd'T'HH:mm:ss",
                  "yyyy-MM-dd' 'HH:mm:ss",
                  "yyyy-MM-dd' 'HH:mm:ss.SSSSSS",
                  "mm/dd/yy' 'HH:mm:ss"],
 'dynamic': True,
 'dynamic_templates': [{'everything_else': {'mapping': {'{name}': {'index': 'not_analyzed',
                                                                   'type': 'string'}},
                                            'match': '*',
                                            'match_mapping_type': 'string'}}],
 'ignore_malformed': True,
 'properties': {'actions': {'dynamic': True,
                            'properties': {'action_type': {'type': 'string'},
                                           'attachments': {'dynamic': False,
                                                           'properties': {'attachment_from': {'type': 'string'},
                                                                          'attachment_name': {'type': 'string'},
                                                                          'attachment_properties': {'dynamic': False,
                                                                                                    'type': 'object'},
                                                                          'attachment_size': {'type': 'long'},
                                                                          'attachment_src': {'type': 'string'},
                                                                          'doc_type': {'index': 'not_analyzed',
                                                                                       'type': 'string'},
                                                                          'identifier': {'type': 'string'},
                                                                          'server_md5': {'type': 'string'},
                                                                          'server_mime': {'type': 'string'}},
                                                           'type': 'object'},
                                           'date': {'format': "yyyy-MM-dd||yyyy-MM-dd'T'HH:mm:ssZZ||yyyy-MM-dd'T'HH:mm:ss.SSSSSS||yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'||yyyy-MM-dd'T'HH:mm:ss'Z'||yyyy-MM-dd'T'HH:mm:ssZ||yyyy-MM-dd'T'HH:mm:ssZZ'Z'||yyyy-MM-dd'T'HH:mm:ss.SSSZZ||yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss.SSSSSS||mm/dd/yy' 'HH:mm:ss",
                                                    'type': 'date'},
                                           'doc_type': {'index': 'not_analyzed',
                                                        'type': 'string'},
                                           'indices': {'dynamic': False,
                                                       'properties': {'doc_type': {'index': 'not_analyzed',
                                                                                   'type': 'string'},
                                                                      'identifier': {'type': 'string'},
                                                                      'referenced_id': {'type': 'string'},
                                                                      'referenced_type': {'type': 'string'}},
                                                       'type': 'object'},
                                           'server_date': {'format': "yyyy-MM-dd||yyyy-MM-dd'T'HH:mm:ssZZ||yyyy-MM-dd'T'HH:mm:ss.SSSSSS||yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'||yyyy-MM-dd'T'HH:mm:ss'Z'||yyyy-MM-dd'T'HH:mm:ssZ||yyyy-MM-dd'T'HH:mm:ssZZ'Z'||yyyy-MM-dd'T'HH:mm:ss.SSSZZ||yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss.SSSSSS||mm/dd/yy' 'HH:mm:ss",
                                                           'type': 'date'},
                                           'sync_log_id': {'type': 'string'},
                                           'updated_known_properties': {'dynamic': False,
                                                                        'type': 'object'},
                                           'updated_unknown_properties': {'dynamic': False,
                                                                          'type': 'object'},
                                           'user_id': {'type': 'string'},
                                           'xform_id': {'type': 'string'},
                                           'xform_name': {'type': 'string'},
                                           'xform_xmlns': {'type': 'string'}},
                            'type': 'nested'},
                'case_attachments': {'dynamic': True,
                                     'properties': {'attachment_from': {'type': 'string'},
                                                    'attachment_name': {'type': 'string'},
                                                    'attachment_properties': {'dynamic': False,
                                                                              'type': 'object'},
                                                    'attachment_size': {'type': 'long'},
                                                    'attachment_src': {'type': 'string'},
                                                    'doc_type': {'index': 'not_analyzed',
                                                                 'type': 'string'},
                                                    'identifier': {'type': 'string'},
                                                    'server_md5': {'type': 'string'},
                                                    'server_mime': {'type': 'string'}},
                                     'type': 'object'},
                'closed': {'type': 'boolean'},
                'closed_by': {'type': 'string'},
                'closed_on': {'format': "yyyy-MM-dd||yyyy-MM-dd'T'HH:mm:ssZZ||yyyy-MM-dd'T'HH:mm:ss.SSSSSS||yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'||yyyy-MM-dd'T'HH:mm:ss'Z'||yyyy-MM-dd'T'HH:mm:ssZ||yyyy-MM-dd'T'HH:mm:ssZZ'Z'||yyyy-MM-dd'T'HH:mm:ss.SSSZZ||yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss.SSSSSS||mm/dd/yy' 'HH:mm:ss",
                              'type': 'date'},
                'computed_': {'enabled': False, 'type': 'object'},
                'computed_modified_on_': {'format': "yyyy-MM-dd||yyyy-MM-dd'T'HH:mm:ssZZ||yyyy-MM-dd'T'HH:mm:ss.SSSSSS||yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'||yyyy-MM-dd'T'HH:mm:ss'Z'||yyyy-MM-dd'T'HH:mm:ssZ||yyyy-MM-dd'T'HH:mm:ssZZ'Z'||yyyy-MM-dd'T'HH:mm:ss.SSSZZ||yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss.SSSSSS||mm/dd/yy' 'HH:mm:ss",
                                          'type': 'date'},
                'doc_type': {'index': 'not_analyzed', 'type': 'string'},
                'domain': {'fields': {'domain': {'index': 'analyzed',
                                                 'type': 'string'},
                                      'exact': {'index': 'not_analyzed',
                                                'type': 'string'}},
                           'type': 'multi_field'},
                'export_tag': {'type': 'string'},
                'external_id': {'fields': {'exact': {'index': 'not_analyzed',
                                                     'type': 'string'},
                                           'external_id': {'index': 'analyzed',
                                                           'type': 'string'}},
                                'type': 'multi_field'},
                'indices': {'dynamic': True,
                            'properties': {'doc_type': {'index': 'not_analyzed',
                                                        'type': 'string'},
                                           'identifier': {'type': 'string'},
                                           'referenced_id': {'type': 'string'},
                                           'referenced_type': {'type': 'string'}},
                            'type': 'object'},
                'initial_processing_complete': {'type': 'boolean'},
                'location_': {'type': 'string'},
                'modified_on': {'format': "yyyy-MM-dd||yyyy-MM-dd'T'HH:mm:ssZZ||yyyy-MM-dd'T'HH:mm:ss.SSSSSS||yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'||yyyy-MM-dd'T'HH:mm:ss'Z'||yyyy-MM-dd'T'HH:mm:ssZ||yyyy-MM-dd'T'HH:mm:ssZZ'Z'||yyyy-MM-dd'T'HH:mm:ss.SSSZZ||yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss.SSSSSS||mm/dd/yy' 'HH:mm:ss",
                                'type': 'date'},
                'name': {'fields': {'exact': {'index': 'not_analyzed',
                                              'type': 'string'},
                                    'name': {'index': 'analyzed',
                                             'type': 'string'}},
                         'type': 'multi_field'},
                'opened_by': {'type': 'string'},
                'opened_on': {'format': "yyyy-MM-dd||yyyy-MM-dd'T'HH:mm:ssZZ||yyyy-MM-dd'T'HH:mm:ss.SSSSSS||yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'||yyyy-MM-dd'T'HH:mm:ss'Z'||yyyy-MM-dd'T'HH:mm:ssZ||yyyy-MM-dd'T'HH:mm:ssZZ'Z'||yyyy-MM-dd'T'HH:mm:ss.SSSZZ||yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss.SSSSSS||mm/dd/yy' 'HH:mm:ss",
                              'type': 'date'},
                'owner_id': {'type': 'string'},
                'referrals': {'enabled': False, 'type': 'object'},
                'server_modified_on': {'format': "yyyy-MM-dd||yyyy-MM-dd'T'HH:mm:ssZZ||yyyy-MM-dd'T'HH:mm:ss.SSSSSS||yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'||yyyy-MM-dd'T'HH:mm:ss'Z'||yyyy-MM-dd'T'HH:mm:ssZ||yyyy-MM-dd'T'HH:mm:ssZZ'Z'||yyyy-MM-dd'T'HH:mm:ss.SSSZZ||yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss.SSSSSS||mm/dd/yy' 'HH:mm:ss",
                                       'type': 'date'},
                'type': {'fields': {'exact': {'index': 'not_analyzed',
                                              'type': 'string'},
                                    'type': {'index': 'analyzed',
                                             'type': 'string'}},
                         'type': 'multi_field'},
                'user_id': {'type': 'string'},
                'version': {'type': 'string'},
                'xform_ids': {'index': 'not_analyzed', 'type': 'string'}}}