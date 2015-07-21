from __future__ import print_function


def generate_script(header_dict, details_dict, searchString=None):
    # TODO: Docstring and comments.
    method = details_dict['method'].strip()
    host = details_dict['Host']
    headers = str(header_dict)
    if searchString:
        try:
            if 'proxy' not in details_dict:
                    skeleton_code = '''\
<?php
$curl = curl_init();
curl_setopt_array($curl, array(
        CURLOPT_RETURNTRANSFER => 1,
        CURLOPT_URL => '''+"'"+host+"',"+'''
));
$response = curl_exec($curl);
curl_close($curl);
return $response
?>'''
            else:
                skeleton_code = '''\
<?php
$curl = curl_init();
curl_setopt_array($curl, array(
        CURLOPT_RETURNTRANSFER => 1,
        CURLOPT_URL => '''+"'"+host+"',"+'''
));
$response = curl_exec($curl);
curl_close($curl);
return $response
?>'''

        except IndexError:
            print("You haven't given the port Number")
        else:
            return skeleton_code
    else:
        try:
            if 'proxy' not in details_dict:
                skeleton_code = '''\
<?php
$curl = curl_init();
curl_setopt_array($curl, array(
        CURLOPT_RETURNTRANSFER => 1,
        CURLOPT_URL => '''+"'"+host+"',"+'''
));
$response = curl_exec($curl);
curl_close($curl);
return $response
?>'''
            else:
                skeleton_code = '''\
<?php
$curl = curl_init();
curl_setopt_array($curl, array(
        CURLOPT_RETURNTRANSFER => 1,
        CURLOPT_URL => '''+"'"+host+"',"+'''
));
$response = curl_exec($curl);
curl_close($curl);
return $response
?>'''
        except IndexError:
            print("You haven't given the port Number")
        else:
            return skeleton_code
