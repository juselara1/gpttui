#!/bin/bash

function test () {
    local file_name=`echo $1 | awk -F '-' '{print $2}'`
    pytest "test/test_${file_name}.py"
}

$*
exit 0
