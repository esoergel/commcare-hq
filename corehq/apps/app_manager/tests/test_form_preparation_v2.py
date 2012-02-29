from casexml.apps.case.tests.util import check_xml_line_by_line
from corehq.apps.app_manager.const import APP_V2
from corehq.apps.app_manager.models import Application, OpenCaseAction, UpdateCaseAction
from django.test import TestCase

XFORM_SOURCE = """<?xml version="1.0" encoding="UTF-8" ?>
<h:html xmlns:h="http://www.w3.org/1999/xhtml" xmlns:orx="http://openrosa.org/jr/xforms" xmlns="http://www.w3.org/2002/xforms" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:jr="http://openrosa.org/javarosa">
	<h:head>
		<h:title>New Form</h:title>
		<model>
			<instance>
				<data xmlns:jrm="http://dev.commcarehq.org/jr/xforms" xmlns="http://openrosa.org/formdesigner/A22A5D53-037A-48DE-979B-BAA54734194E" uiVersion="1" version="1" name="New Form">
					<question1 />
				</data>
			</instance>
			<bind nodeset="/data/question1" type="xsd:string" />
			<itext>
				<translation lang="en" default="">
					<text id="question1-label">
						<value>question1</value>
					</text>
				</translation>
			</itext>
		</model>
	</h:head>
	<h:body>
		<input ref="/data/question1">
			<label ref="jr:itext('question1-label')" />
		</input>
	</h:body>
</h:html>
"""

OPEN_CASE_SOURCE = """<?xml version="1.0"?>
<h:html xmlns:h="http://www.w3.org/1999/xhtml" xmlns:orx="http://openrosa.org/jr/xforms" xmlns="http://www.w3.org/2002/xforms" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:jr="http://openrosa.org/javarosa">
	<h:head>
		<h:title>New Form</h:title>
		<model>
			<instance>
				<data xmlns:jrm="http://dev.commcarehq.org/jr/xforms" xmlns="http://openrosa.org/formdesigner/A22A5D53-037A-48DE-979B-BAA54734194E" uiVersion="1" version="3" name="New Form">
					<question1/>
					<case xmlns="http://commcarehq.org/case/transaction/v2" case_id="" user_id="" date_modified="">
						<create>
							<case_name/>
							<case_type>test_case_type</case_type>
						</create>
					</case>
					<orx:meta>
						<orx:deviceID/>
						<orx:timeStart/>
						<orx:timeEnd/>
						<orx:username/>
						<orx:userID/>
						<orx:instanceID/>
					</orx:meta>
				</data>
			</instance>
			<bind nodeset="/data/question1" type="xsd:string" required="true()"/>
			<itext>
				<translation lang="en" default="">
					<text id="question1-label">
						<value>question1</value>
					</text>
				</translation>
			</itext>
            <instance src="jr://instance/session" id="commcaresession"/>
			<bind nodeset="case/@date_modified" type="dateTime" calculate="/data/meta/timeEnd"/>
			<setvalue ref="case/@case_id" event="xforms-ready" value="uuid()"/>
			<bind nodeset="case/@user_id" calculate="/data/meta/userID"/>
			<bind nodeset="case/create/case_name" calculate="/data/question1"/>
			<setvalue ref="/data/meta/deviceID" event="xforms-ready" value="instance('commcaresession')/session/context/deviceid"/>
			<setvalue ref="/data/meta/timeStart" event="xforms-ready" value="now()"/>
			<bind nodeset="meta/timeStart" type="xsd:dateTime"/>
			<setvalue ref="/data/meta/timeEnd" event="xforms-revalidate" value="now()"/>
			<bind nodeset="meta/timeEnd" type="xsd:dateTime"/>
			<setvalue ref="/data/meta/username" event="xforms-ready" value="instance('commcaresession')/session/context/username"/>
			<setvalue ref="/data/meta/userID" event="xforms-ready" value="instance('commcaresession')/session/context/userid"/>
			<setvalue ref="/data/meta/instanceID" event="xforms-ready" value="uuid()"/>
		</model>
	</h:head>
	<h:body>
		<input ref="/data/question1">
			<label ref="jr:itext('question1-label')"/>
		</input>
	</h:body>
</h:html>
"""

OPEN_CASE_EXTERNAL_ID_SOURCE = """<?xml version="1.0"?>
<h:html xmlns:h="http://www.w3.org/1999/xhtml" xmlns:orx="http://openrosa.org/jr/xforms" xmlns="http://www.w3.org/2002/xforms" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:jr="http://openrosa.org/javarosa">
	<h:head>
		<h:title>New Form</h:title>
		<model>
			<instance>
				<data xmlns:jrm="http://dev.commcarehq.org/jr/xforms" xmlns="http://openrosa.org/formdesigner/A22A5D53-037A-48DE-979B-BAA54734194E" uiVersion="1" version="3" name="New Form">
					<question1/>
					<case xmlns="http://commcarehq.org/case/transaction/v2" case_id="" user_id="" date_modified="">
						<create>
							<case_name/>
							<case_type>test_case_type</case_type>
						</create>
						<update>
							<external_id/>
						</update>
					</case>
					<orx:meta>
						<orx:deviceID/>
						<orx:timeStart/>
						<orx:timeEnd/>
						<orx:username/>
						<orx:userID/>
						<orx:instanceID/>
					</orx:meta>
				</data>
			</instance>
			<bind nodeset="/data/question1" type="xsd:string" required="true()"/>
			<itext>
				<translation lang="en" default="">
					<text id="question1-label">
						<value>question1</value>
					</text>
				</translation>
			</itext>
            <instance src="jr://instance/session" id="commcaresession"/>
			<bind nodeset="case/@date_modified" type="dateTime" calculate="/data/meta/timeEnd"/>
			<setvalue ref="case/@case_id" event="xforms-ready" value="uuid()"/>
			<bind nodeset="case/@user_id" calculate="/data/meta/userID"/>
			<bind nodeset="case/create/case_name" calculate="/data/question1"/>
			<bind nodeset="case/update/external_id" calculate="/data/question1"/>
			<setvalue ref="/data/meta/deviceID" event="xforms-ready" value="instance('commcaresession')/session/context/deviceid"/>
			<setvalue ref="/data/meta/timeStart" event="xforms-ready" value="now()"/>
			<bind nodeset="meta/timeStart" type="xsd:dateTime"/>
			<setvalue ref="/data/meta/timeEnd" event="xforms-revalidate" value="now()"/>
			<bind nodeset="meta/timeEnd" type="xsd:dateTime"/>
			<setvalue ref="/data/meta/username" event="xforms-ready" value="instance('commcaresession')/session/context/username"/>
			<setvalue ref="/data/meta/userID" event="xforms-ready" value="instance('commcaresession')/session/context/userid"/>
			<setvalue ref="/data/meta/instanceID" event="xforms-ready" value="uuid()"/>
		</model>
	</h:head>
	<h:body>
		<input ref="/data/question1">
			<label ref="jr:itext('question1-label')"/>
		</input>
	</h:body>
</h:html>
"""
UPDATE_CASE_SOURCE = """<?xml version="1.0"?>
<h:html xmlns:h="http://www.w3.org/1999/xhtml" xmlns:orx="http://openrosa.org/jr/xforms" xmlns="http://www.w3.org/2002/xforms" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:jr="http://openrosa.org/javarosa">
	<h:head>
		<h:title>New Form</h:title>
		<model>
			<instance>
				<data xmlns:jrm="http://dev.commcarehq.org/jr/xforms" xmlns="http://openrosa.org/formdesigner/A22A5D53-037A-48DE-979B-BAA54734194E" uiVersion="1" version="3" name="New Form">
					<question1/>
					<case xmlns="http://commcarehq.org/case/transaction/v2" case_id="" user_id="" date_modified="">
						<update>
							<question1/>
						</update>
					</case>
					<orx:meta>
						<orx:deviceID/>
						<orx:timeStart/>
						<orx:timeEnd/>
						<orx:username/>
						<orx:userID/>
						<orx:instanceID/>
					</orx:meta>
				</data>
			</instance>
			<bind nodeset="/data/question1" type="xsd:string"/>
			<itext>
				<translation lang="en" default="">
					<text id="question1-label">
						<value>question1</value>
					</text>
				</translation>
			</itext>
            <instance src="jr://instance/session" id="commcaresession"/>
			<bind nodeset="case/@date_modified" type="dateTime" calculate="/data/meta/timeEnd"/>
			<bind nodeset="case/@case_id" calculate="instance('commcaresession')/session/data/case_id"/>
			<bind nodeset="case/update/question1" relevant="count(/data/question1) &gt; 0" calculate="/data/question1"/>
			<setvalue ref="/data/meta/deviceID" event="xforms-ready" value="instance('commcaresession')/session/context/deviceid"/>
			<setvalue ref="/data/meta/timeStart" event="xforms-ready" value="now()"/>
			<bind nodeset="meta/timeStart" type="xsd:dateTime"/>
			<setvalue ref="/data/meta/timeEnd" event="xforms-revalidate" value="now()"/>
			<bind nodeset="meta/timeEnd" type="xsd:dateTime"/>
			<setvalue ref="/data/meta/username" event="xforms-ready" value="instance('commcaresession')/session/context/username"/>
			<setvalue ref="/data/meta/userID" event="xforms-ready" value="instance('commcaresession')/session/context/userid"/>
			<setvalue ref="/data/meta/instanceID" event="xforms-ready" value="uuid()"/>
		</model>
	</h:head>
	<h:body>
		<input ref="/data/question1">
			<label ref="jr:itext('question1-label')"/>
		</input>
	</h:body>
</h:html>
"""

OPEN_UPDATE_CASE_SOURCE = """<?xml version="1.0"?>
<h:html xmlns:h="http://www.w3.org/1999/xhtml" xmlns:orx="http://openrosa.org/jr/xforms" xmlns="http://www.w3.org/2002/xforms" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:jr="http://openrosa.org/javarosa">
	<h:head>
		<h:title>New Form</h:title>
		<model>
			<instance>
				<data xmlns:jrm="http://dev.commcarehq.org/jr/xforms" xmlns="http://openrosa.org/formdesigner/A22A5D53-037A-48DE-979B-BAA54734194E" uiVersion="1" version="3" name="New Form">
					<question1/>
					<case xmlns="http://commcarehq.org/case/transaction/v2" case_id="" user_id="" date_modified="">
						<create>
							<case_name/>
							<case_type>test_case_type</case_type>
						</create>
						<update>
							<question1/>
						</update>
					</case>
					<orx:meta>
						<orx:deviceID/>
						<orx:timeStart/>
						<orx:timeEnd/>
						<orx:username/>
						<orx:userID/>
						<orx:instanceID/>
					</orx:meta>
				</data>
			</instance>
			<bind nodeset="/data/question1" type="xsd:string" required="true()"/>
			<itext>
				<translation lang="en" default="">
					<text id="question1-label">
						<value>question1</value>
					</text>
				</translation>
			</itext>
            <instance src="jr://instance/session" id="commcaresession"/>
			<bind nodeset="case/@date_modified" type="dateTime" calculate="/data/meta/timeEnd"/>
			<setvalue ref="case/@case_id" event="xforms-ready" value="uuid()"/>
			<bind nodeset="case/@user_id" calculate="/data/meta/userID"/>
			<bind nodeset="case/create/case_name" calculate="/data/question1"/>
			<bind nodeset="case/update/question1" relevant="count(/data/question1) &gt; 0" calculate="/data/question1"/>
			<setvalue ref="/data/meta/deviceID" event="xforms-ready" value="instance('commcaresession')/session/context/deviceid"/>
			<setvalue ref="/data/meta/timeStart" event="xforms-ready" value="now()"/>
			<bind nodeset="meta/timeStart" type="xsd:dateTime"/>
			<setvalue ref="/data/meta/timeEnd" event="xforms-revalidate" value="now()"/>
			<bind nodeset="meta/timeEnd" type="xsd:dateTime"/>
			<setvalue ref="/data/meta/username" event="xforms-ready" value="instance('commcaresession')/session/context/username"/>
			<setvalue ref="/data/meta/userID" event="xforms-ready" value="instance('commcaresession')/session/context/userid"/>
			<setvalue ref="/data/meta/instanceID" event="xforms-ready" value="uuid()"/>
		</model>
	</h:head>
	<h:body>
		<input ref="/data/question1">
			<label ref="jr:itext('question1-label')"/>
		</input>
	</h:body>
</h:html>
"""

class FormPreparationV2Test(TestCase):
    def setUp(self):
        self.app = Application.new_app('domain', 'New App', APP_V2)
        self.app.version = 3
        self.module = self.app.new_module('New Module', lang='en')
        self.form = self.app.new_form(0, 'New Form', lang='en')
        self.module.case_type = 'test_case_type'

    def test_open_case(self):
        self.form.source = XFORM_SOURCE
        self.form.actions.open_case = OpenCaseAction(name_path="/data/question1", external_id=None)
        self.form.actions.open_case.condition.type = 'always'
        check_xml_line_by_line(self, OPEN_CASE_SOURCE, self.form.render_xform())

    def test_open_case_external_id(self):
        self.form.source = XFORM_SOURCE
        self.form.actions.open_case = OpenCaseAction(name_path="/data/question1", external_id='/data/question1')
        self.form.actions.open_case.condition.type = 'always'
        check_xml_line_by_line(self, OPEN_CASE_EXTERNAL_ID_SOURCE, self.form.render_xform())

    def test_update_case(self):
        self.form.source = XFORM_SOURCE
        self.form.requires = 'case'
        self.form.actions.update_case = UpdateCaseAction(update={'question1': '/data/question1'})
        self.form.actions.update_case.condition.type = 'always'
        check_xml_line_by_line(self, UPDATE_CASE_SOURCE, self.form.render_xform())

    def test_open_update_case(self):
        self.form.source = XFORM_SOURCE
        self.form.actions.open_case = OpenCaseAction(name_path="/data/question1", external_id=None)
        self.form.actions.open_case.condition.type = 'always'
        self.form.actions.update_case = UpdateCaseAction(update={'question1': '/data/question1'})
        self.form.actions.update_case.condition.type = 'always'
        check_xml_line_by_line(self, OPEN_UPDATE_CASE_SOURCE, self.form.render_xform())