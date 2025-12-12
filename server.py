<!DOCTYPE html>
<html>
<head>
    <title>Simple Python Web</title>
</head>
<body>
<h2>Form Input Data</h2>
<form action="/save" method="post">
    <label>Nama:</label><br>
    <input type="text" name="name"><br><br>

    <label>Email:</label><br>
    <input type="email" name="email"><br><br>

    <input type="submit" value="Submit">
</form>

<br>
<a href="/users"> Lihat Data</a>
</body>
</html>
