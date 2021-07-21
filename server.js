const express = require('express');
const multer = require('multer');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');
const app = express();
var path = require('path');
const PORT = process.env.PORT || 8080;

app.use(cors({credentials: true, origin: 'http://localhost:3000'}));


const storage =
    multer.diskStorage({
        destination: 'incomingPDF/', // destination folder
        filename: (req, file, cb) => {
            let uuid = uuidv4();
            let pdfName = uuid + path.extname(file.originalname);
            cb(null, pdfName);
        }
    });

const upload = multer({
        storage,
        dest: "incomingPDF/", // destination folder
        limits: {fileSize: 3500000}, // size we will acept, not bigger
        fileFilter: (req, file, cb) => {
            console.log(file);
            const filetypes = /pdf/; // filetypes you will accept
            const mimetype = filetypes.test(file.mimetype); // verify file is == filetypes you will accept
            const extname = filetypes.test(path.extname(file.originalname)); // extract the file extension
            // if mimetype && extname are true, then no error
            if(mimetype){
                return cb(null, true);
            }
            // if mimetype or extname false, give an error of compatibilty
            return cb("The uploaded file, isn't compatible :( we're sorry");
        }
    }).single('pdfFile'); // This is the field where is the input type="file", we only accept 1 image

app.use(upload);

app.post("/check", async(req,res)=>{
    if(req.body.givenText !== undefined){
        let uuid = uuidv4();
        fs.appendFile(`textFiles/${uuid+'.txt'}`, req.body.givenText, (err)=>{
            if(err)
                throw err;
            console.log("filesaved");
        })
    }
})

app.listen(PORT, ()=>{
    console.log(`Server is running at PORT: ${PORT}`);
})
