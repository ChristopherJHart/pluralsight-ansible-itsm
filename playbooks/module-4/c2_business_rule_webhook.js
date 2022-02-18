(function executeRule(current, previous /*null when async*/) {
    try {
        var r = new sn_ws.RESTMessageV2();

        // getValue(string) does not support dot walking,
        // so I had to do a bit more to get the user's email address
        var usr = new GlideRecord('sys_user');
        usr.get('sys_id', current.getValue("caller_id"));
        var reported_by_email = usr.getValue('email');

        // Make sure to convert object references to values.
        // More info at:
        // https://swissbytes.blogspot.com/2017/11/service-now-script-includes-make-sure.html

        var number = current.getValue("number");
        var opened_at = current.getValue("opened_at");
        var impact = current.getValue("impact");
        var urgency = current.getValue("urgency");
        var short_description = current.getValue("short_description");
        var description = current.getValue("description");
        var category = current.getValue("category");
        var priority = current.getValue("priority");
        var sys_id = current.getValue("sys_id");
        var subcategory = current.getValue("subcategory");
        var state = current.getValue("state");
        var source_ip = current.getValue("u_source_ip");
        var destination_ip = current.getValue("u_destination_ip");

        var obj = {
            "number": number,
            "reported_by_email": reported_by_email,
            "opened_at": opened_at,
            "impact": impact,
            "urgency": urgency,
            "short_description": short_description,
            "description": description,
            "category": category,
            "priority": priority,
            "sys_id": sys_id,
            "subcategory": subcategory,
            "state": state,
            "source_ip": source_ip,
            "destination_ip": destination_ip
        };

        r.setEndpoint("http://itsm-automation.chrisjhart.com/servicenow/" + number);
        r.setHttpMethod("post");

        var body = JSON.stringify(obj);
        gs.info("Webhook body: " + body);
        r.setRequestBody(body);

        var response = r.execute();
        var httpStatus = response.getStatusCode();
    } catch (ex) {
        var message = ex.message;
        gs.error("Error message: " + message);
    }

    gs.info("Webhook target HTTP status response: " + httpStatus);
    gs.info("Webhook response: " + response.getBody());

})(current, previous);
