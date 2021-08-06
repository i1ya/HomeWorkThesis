'use strict';

function theses_load() {

    let theses_list = document.getElementById('ThesisList');
    let wt_select = document.getElementById('levels');
    let page = url.searchParams.get("page");
    let supervisor_select = document.getElementById('supervisor');
    let department_select = document.getElementById('department');

    let params = new URLSearchParams();
    let wt = wt_select.value;

    // Page first
    if (page && page > 1){
        params.append('page', page);
    }

    // Department?
    if (department_select){
        params.append('department', department_select.value);
    }

    // Supervisor?
    if (supervisor_select){
        params.append('supervisor', supervisor_select.value);
    }

    if (wt > 1)
    {
        params.append('levels', wt);
    }


    fetch('fetch_themes?' + params.toString()).then(function(response){

        if (!response.ok){
            window.location.href = '/404.html'
        } else {
            response.text().then(function (text) {
                theses_list.innerHTML = text;
                $('[data-toggle="popoverhover"]').popover({ trigger: "hover" });
            });
        }
    });
}


//
// Update theses list
//

function theses_update() {

    let theses_list = document.getElementById('ThesisList');
    let wt_select = document.getElementById('levels');
    let supervisor_select = document.getElementById('supervisor');
    let department_select = document.getElementById('department');

    let params = new URLSearchParams();
    let wt = wt_select.value;

    if (wt > 1)
    {
        params.append('levels', wt);
    }

    // If supervisor?
    if (supervisor_select){
        params.append('supervisor', supervisor_select.value);
    }

    // Department?
    if (department_select){
        params.append('department', department_select.value);
    }

    if (Array.from(params).length){
        window.history.pushState("", "", 'theses.html?' + params.toString());
    } else {
        window.history.pushState("", "", 'theses.html');
    }

    fetch('fetch_theses?' + params.toString()).then(function(response){

        if (!response.ok){
            window.location.href = '/404.html'
        } else {
            response.text().then(function (text) {
                theses_list.innerHTML = text;
                $('[data-toggle="popoverhover"]').popover({ trigger: "hover" });
            });
        }

    });
}

// Select filters
let wt_select = document.getElementById('levels');
let supervisor_select = document.getElementById('supervisor');
let department_select = document.getElementById('department');

// Get filters from URI
let url_string = window.location.href
let url = new URL(url_string);
let levels = url.searchParams.get("levels");
let page = url.searchParams.get("page");
let supervisor = url.searchParams.get("supervisor");
let department = url.searchParams.get("department");

if (wt_select)
{
    // Set filter to value from URI
    if (levels && levels <= wt_select.length && levels > 0){
        wt_select.value=levels;
    }

    if (supervisor){

        // Check if this value exist
        if (supervisor_select.innerHTML.indexOf('value="' + supervisor + '"') > -1){
            supervisor_select.value=supervisor;
        } else {
            supervisor_select.value=0;
        }
    }

    if (department > 0){
        department_select.value=department;
    }


    // Load theses
    theses_load();

    // Update theses
    wt_select.onchange = theses_update;
    supervisor_select.onchange = theses_update;
    department_select.onchange = theses_update;
}
