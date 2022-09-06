<?php
include "functions/database.php";

$data = $db->query("SELECT * FROM settings");
$info = $db->fetch_array($data);
?>
<!DOCTYPE html>
<html class="full" lang="en">

    <head>
		<base href="<?php echo $info['URL']; ?>/" />
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="">
        <meta name="author" content="">

        <title>Api - <?php echo $info['name']; ?></title>

        <!-- Bootstrap core CSS -->
        <link href="css/bootstrap.css" rel="stylesheet">

        <!-- Custom CSS for the Template -->
        <link href="css/style.css" rel="stylesheet">
        <link href="css/animate.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css?family=Fjalla+One" rel="stylesheet">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.1/css/all.css" integrity="sha384-5sAR7xN1Nv6T6+dT2mhtzEpVJvfS3NScPQTrOxhwjIuvcA67KV2R5Jz6kr4abQsz" crossorigin="anonymous">
        <style>
            <?php echo $info['cstm-style']; ?>
        </style>
    </head>

    <body>
        <?php
            include "functions/menu.php";
        ?>
        <div class="container">
            <div class="row logo">
                <div class="col-lg-12" style="text-align:center">
                    <?php 
                        include "functions/logo.php";
                        include "functions/darkmode.php";
                    ?>
                </div>
            </div>
        </div>
        <div class="container  animated fadeIn">

            <div class="row" style="margin-top: -25px;">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h2 class="modal-title" id="myModalLabel">Developer Api</h2>
                        </div>
                        <div class="modal-body" style="min-height:10%; max-height:350px; overflow-y:scroll; overflow-x:none; position:relative;">
                            <h4 class="text-center">You can use our API to create Shortned URLs for any use </h4>
                            <br>
                            <h5><strong>Basic URL</strong> </h5>
                            <div style="margin-left:25px;">
                                <h5>Input <strong><?php echo $info['URL'] . '/api.php?url=XXX'; ?> </h5>								
                                <h5><strong>XXX</strong> is your <strong>URL </strong> it should be valid, starting with <strong>http:// OR https://</h5>								
                                <h5>Output <strong><?php echo $info['URL'] . '/{alias}'; ?> </h5>	
                            </div>
                            <br>
                            <h5><strong>URL with custom link</strong> </h5>
                            <div style="margin-left:25px;">
                                <h5>Input <strong><?php echo $info['URL'] . '/api.php?url=XXX&cust=YYY'; ?> </h5>								
                                <h5><strong>XXX</strong> is your v it should be valid, starting with <strong>http:// OR https://</h5>								
                                <h5><strong>YYY</strong> is your <strong>Custom link </strong> Which should be only Alphanumeric (Underscore and Dash Is allowed)</h5>								
                                <h5>Output <strong><?php echo $info['URL'] . '/YYY'; ?> </h5>	
                            </div>
                            <br>
                            <h5><strong>URL with Password</strong> </h5>
                            <div style="margin-left:25px;">
                                <h5>Input <strong><?php echo $info['URL'] . '/api.php?url=XXX&pass=ZZZ'; ?> </h5>								
                                <h5><strong>XXX</strong> is your <strong>URL </strong> it should be valid, starting with <strong>http:// OR https://</h5>								
                                <h5><strong>ZZZ</strong> is your <strong>Password </strong> Which should be only Alphanumeric (Underscore and Dash Is allowed)</h5>								
                                <h5>Output <strong><?php echo $info['URL'] . '/{alias}'; ?> </h5>	
                            </div>
                            <br>
                            <h5><strong>URL with Custom Link and Password</strong> </h5>
                            <div style="margin-left:25px;">
                                <h5>Input <strong><?php echo $info['URL'] . '/api.php?url=XXX&cust=YYY&pass=ZZZ'; ?> </h5>								
                                <h5><strong>XXX</strong> is your <strong>URL </strong> it should be valid, starting with <strong>http:// OR https://</h5>								
                                <h5><strong>YYY</strong> is your <strong>Custom link </strong> Which should be only Alphanumeric (Underscore and Dash Is allowed)</h5>								                                   
                                <h5><strong>ZZZ</strong> is your <strong>Password </strong> Which should be only Alphanumeric (Underscore and Dash Is allowed)</h5>								
                                <h5>Output <strong><?php echo $info['URL'] . '/YYY'; ?> </h5>									
                            </div>
                        </div>
                    </div>

                </div><!-- /.modal-content -->
            </div>
        </div>


    </div>
    <!-- JavaScript -->
    <script src="js/jquery-1.10.2.js"></script>
    <script src="js/bootstrap.js"></script>

</body>

</html>
