let parameters = {};
function pushParameter (name, v) {
    if (!parameters [name]) {
        parameters [name] = [];
    }
    parameters [name].push (v);
}
function popParameter (name) {
    parameters [name].pop ();
}
function getParameter (name) {
    return parameters [name];
}


let _rewrite = {

text : function (chars,) {
enter_rule ("text");
    set_return (`${chars.rwr ().join ('')}`);
return exit_rule ("text");
},
char_unicodestring : function (s,) {
enter_rule ("char_unicodestring");
    set_return (`${s.rwr ()}`);
return exit_rule ("char_unicodestring");
},
char_comment : function (lb,cs,rb,) {
enter_rule ("char_comment");
    set_return (`#${cs.rwr ().join ('')}`);
return exit_rule ("char_comment");
},
char_errormessage : function (lb,cs,rb,) {
enter_rule ("char_errormessage");
    set_return (` >>> ${cs.rwr ().join ('')} <<< `);
return exit_rule ("char_errormessage");
},
char_line : function (lb,cs,rb,) {
enter_rule ("char_line");
    set_return (`#line ${cs.rwr ().join ('')}`);
return exit_rule ("char_line");
},
char_other : function (c,) {
enter_rule ("char_other");
    set_return (`${c.rwr ()}`);
return exit_rule ("char_other");
},
historical_edge_case_ulb : function (c,) {
enter_rule ("historical_edge_case_ulb");
    set_return (``);
return exit_rule ("historical_edge_case_ulb");
},
historical_edge_case_encodedulb : function (c,) {
enter_rule ("historical_edge_case_encodedulb");
    set_return (`_L`);
return exit_rule ("historical_edge_case_encodedulb");
},
historical_edge_case_urb : function (c,) {
enter_rule ("historical_edge_case_urb");
    set_return (``);
return exit_rule ("historical_edge_case_urb");
},
historical_edge_case_encodedurb : function (c,) {
enter_rule ("historical_edge_case_encodedurb");
    set_return (`R_`);
return exit_rule ("historical_edge_case_encodedurb");
},
historical_edge_case_space : function (c,) {
enter_rule ("historical_edge_case_space");
    set_return (`_`);
return exit_rule ("historical_edge_case_space");
},
historical_edge_case_tab : function (c,) {
enter_rule ("historical_edge_case_tab");
    set_return (`	`);
return exit_rule ("historical_edge_case_tab");
},
historical_edge_case_newline : function (c,) {
enter_rule ("historical_edge_case_newline");
    set_return (`
`);
return exit_rule ("historical_edge_case_newline");
},
historical_edge_case_paramark : function (c,) {
enter_rule ("historical_edge_case_paramark");
    set_return (`¶`);
return exit_rule ("historical_edge_case_paramark");
},
unicode_string : function (lq,cs,rq,) {
enter_rule ("unicode_string");
    set_return (`${lq.rwr ()}${cs.rwr ().join ('')}${rq.rwr ()}`);
return exit_rule ("unicode_string");
},
ustringchar_nested : function (lq,cs,rq,) {
enter_rule ("ustringchar_nested");
    set_return (`${lq.rwr ()}${cs.rwr ().join ('')}${rq.rwr ()}`);
return exit_rule ("ustringchar_nested");
},
ustringchar_other : function (c,) {
enter_rule ("ustringchar_other");
    set_return (`${c.rwr ()}`);
return exit_rule ("ustringchar_other");
},
_terminal: function () { return this.sourceString; },
_iter: function (...children) { return children.map(c => c.rwr ()); }
}
