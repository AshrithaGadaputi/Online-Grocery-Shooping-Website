//jshint esversion:6
require('dotenv').config()
const express=require('express');
const bodyParser=require('body-parser');
const ejs=require('ejs');
const mongoose=require('mongoose');
const encrypt=require('mongoose-encryption');
const mysql=require('mysql2');
let email = "gadaputiashritha@gmail.com";
const app=express();
var spawn=require("child_process").spawn;
app.use(express.static(__dirname + '/public'))
global.category = "";
console.log(process.env.API_KEY)

app.use(express.static('public'));
app.set('view engine','ejs');
app.use(bodyParser.urlencoded({
    extended:true
}));

//python



app.get("/abc", function(req, res){
    var process2 = spawn("python", [
        "./Collaborative_Filtering.py"
      ]);
      process2.stdout.on("data", function (data2) {
        // res.send(data2.toString());
        res.send(data2);
      });
})


//db connection
mongoose.connect("mongodb://localhost:27017/userDB",{useNewUrlParser:true});

const userSchema=new mongoose.Schema({
    email:String,
    password:String
});


userSchema.plugin(encrypt,{secret:process.env.SECRET,encryptedFields:['password']});

const User=new mongoose.model("User",userSchema)


//mysql db connection
const connection=mysql.createConnection({
    //mysql configuration in json format
    host:'localhost',
    database:'groceryDB',
    user:'root',
    password:'Ashri@2003'
});

connection.connect(function(error){
    if(error)
    {
        throw error;
    }
    else
    {
        console.log('MySQL Database is connected successfully');
    }
});

app.get("/",function(req,res){
    res.render("home");
});

app.get("/login",function(req,res){
    res.render("login");
});

app.get("/register",function(req,res){
    res.render("register");
});



app.post("/register",function(req,res){
    const newUser=new User({
        email:req.body.username,
        password:req.body.password
    });

    newUser.save(function(err){
        if(err){
            console.log(err);
        }else{
            res.render("homepage");
        }
    });
});


app.post("/login",function(req,res){
    const username=req.body.username;
    email = username;
    const password=req.body.password;

    User.findOne({email:username},function(err,foundUser){
        if(err){
            console.log(err);
        }else{
            if(foundUser) {
                if(foundUser.password===password){
                    res.render("homepage")
                }
            }
        }
    });
});

app.get("/FruitsCategoryPage",function(req,res){
    global.category = "fruits";
    //got to database select * from fruits
    var SQL = "SELECT * FROM fruits";
    connection.query(SQL, function(err, result){
        if(!err)
        {
            console.log(result);
            res.render("FruitsCategoryPageHTML", {fruitList : result});
        }
    })
});

app.get("/MedicineCategoryPageHTML",function(req,res){
    global.category = "medicines";
    //got to database select * from fruits
    var SQL = "SELECT * FROM medicine";
    connection.query(SQL, function(err, result){
        if(!err)
        {
            console.log(result);
            res.render("MedicineCategoryPageHTML", {medicineList : result});
        }
    })
});

app.get("/OfficeCategoryPageHTML",function(req,res){
    global.category = "office";
    var SQL = "SELECT * FROM stationary";
    connection.query(SQL, function(err, result){
        if(!err)
        {
            console.log(result);
            res.render("OfficeCategoryPageHTML", {officeList : result});
        }
    })
});


app.post("/ShoppingCartHTML", function(req, res){
    const nameItem = req.body.submit_button;
    var SQL = "INSERT INTO addToCart VALUES ?";
    console.log(email);
    var values = [[email, nameItem, 1]];
    connection.query(SQL, [values], function(err){
        if(!err)
        {
            var SQL2 = "";
            if(global.category == "fruits")
            {
                SQL2 = "SELECT a.name, a.quantity, f.imageurl, f.price FROM addToCart a,fruits f WHERE a.name = f.name and email=?";
            }
            else if(global.category=="medicines")
            {
                SQL2 = "SELECT a.name, a.quantity, m.imageurl, m.price FROM addToCart a, medicine m,fruits f WHERE a.name = m.name and email=?";
            }
            else if(global.category=="office")
            {
                SQL2 = "SELECT a.name, a.quantity, o.imageurl, o.price FROM addToCart a,stationary o WHERE a.name = o.name and email=?";
            }
            console.log(SQL2);
            connection.query(SQL2, email, function(err, result){
                if(!err)
                {
                    console.log(result);
                    res.render("ShoppingCartHTML", {addedList : result});
                }
                
            
            });
            
        }
        
        else
        res.send(err);
    });
});






app.post("/newpage", function(req, res){
    res.render('newpage');
});
app.post("/homepage", function(req, res){
    res.render('homepage');
});



app.get("/ShoppingCartHTML",function(req,res){
    res.render("ShoppingCartHTML");
});



app.listen(3000,function(){
    console.log("Server started on port 3000");
});