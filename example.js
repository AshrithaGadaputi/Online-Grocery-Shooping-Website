var process2 = spawn("python", [
    "./Collaborative_Filtering.py"
  ]);
  process2.stdout.on("data", function (data2) {
    // res.send(data2.toString());
    res.redirect("/generate-report");
  });