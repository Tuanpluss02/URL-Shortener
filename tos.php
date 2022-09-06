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

        <title>Terms - <?php echo $info['name']; ?></title>

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
                            <h2 class="modal-title" id="myModalLabel">Terms &amp; Conditions</h2>
                        </div>
                        <div class="modal-body" style="min-height:10%; max-height:350px; overflow-y:scroll; overflow-x:none; position:relative;">
                            <p>Do not spam the website</p>
                            <p>Do not short virus, malware links</p>
                            <p>Do not short non legal links</p>
                            <p>Do not spam the website, Do not spam the website, Do not spam the website, Do not spam the website</p>
                            <p>Do not spam the website</p>
                            <p>Do not short virus, malware links</p>
                            <p>using service you should know : Lorem ipsum dolor sit amet consectetur adipisicing elit. A, dolores! Iusto sequi sint fuga beatae ex ad ea aliquam perspiciatis ullam harum error, ducimus similique, voluptas doloremque iste esse ipsum. </p>
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
<?php $db->close_connection(); ?>