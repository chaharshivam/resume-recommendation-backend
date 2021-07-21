const express = require('express');
const multer = require('multer');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');
const app = express();
const {PythonShell} = require('python-shell');

var path = require('path');
const PORT = process.env.PORT || 8080;

app.use(cors({credentials: true, origin: 'http://localhost:3000'}));


const storage =
    multer.diskStorage({
        destination: 'incomingFile/', // destination folder
        filename: (req, file, cb) => {
            let uuid = uuidv4();
            let nameOfFile = uuid + path.extname(file.originalname);
            cb(null, nameOfFile);
            runPythonScript(nameOfFile)
        }
    });

const upload = multer({
        storage,
        dest: "incomingFile/", // destination folder
        limits: {fileSize: 3500000}, // size we will acept, not bigger
        fileFilter: (req, file, cb) => {
            console.log(file);
            const filetypes = /pdf|vnd.openxmlformats-officedocument.spreadsheetml.sheet|vnd.ms-excel/; // filetypes you will accept
            console.log(file.mimetype);
            const mimetype = filetypes.test(file.mimetype); // verify file is == filetypes you will accept
            const extname = filetypes.test(path.extname(file.originalname)); // extract the file extension
            // if mimetype && extname are true, then no error
            console.log(mimetype);
            if(mimetype){
                return cb(null, true);
            }
            // if mimetype or extname false, give an error of compatibilty
            return cb("The uploaded file, isn't compatible :( we're sorry");
        }
    }).single('userFile'); // This is the field where is the input type="file"

app.use(upload);

app.post("/check", async(req,res)=>{
    if(req.body.givenText !== undefined){
        let uuid = uuidv4();
        fs.appendFile(`incomingText/${uuid+'.txt'}`, req.body.givenText, (err)=>{
            if(err)
                throw err;
            console.log("filesaved");
        })
    }
})

app.listen(PORT, ()=>{
    console.log(`Server is running at PORT: ${PORT}`);
})

const runPythonScript = function(receivedFileName){
    let options = {
        mode: 'text',
        //pythonOptions: ['-u'], // get print results in real-time
        //scriptPath: 'path/to/my/scripts', //If you are having python_test.py script in same folder, then it's optional.
        args: [`${receivedFileName}`] //An argument which can be accessed in the script using sys.argv[1]
    };
    PythonShell.run('resume_classifier.py',options, function (err, result){
        if (err) throw err;
        // result is an array consisting of messages collected
        //during execution of script.
        for(let i = 0; i<result.length; i++){
            console.log(result[i]);
        }
        //res.send(result.toString())
    });
}
