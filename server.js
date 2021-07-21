const express = require('express');
const multer = require('multer');
const cors = require('cors');
const PORT = process.env.PORT || 8080;
const app = express();
app.use(cors({credentials: true, origin: 'http://localhost:3000'}));

const storage =
    multer.diskStorage({
        destination: 'incomingPDF/', // destination folder
        filename: (req, file, cb) => {
            cb(null, uuid.v4() + path.extname(file.originalname));
        }
    });

const upload = multer({
        storage,
        dest: "incomingPDF/", // destination folder
        limits: {fileSize: 3500000}, // size we will acept, not bigger
        fileFilter: (req, file, cb) => {
            const filetypes = /pdf/; // filetypes you will accept
            const mimetype = filetypes.test(file.mimetype); // verify file is == filetypes you will accept
            const extname = filetypes.test(path.extname(file.originalname)); // extract the file extension
            // if mimetype && extname are true, then no error
            if(mimetype && extname){
                return cb(null, true);
            }
            // if mimetype or extname false, give an error of compatibilty
            return cb("The uploaded file, isn't compatible :( we're sorry");
        }
    }).single('imagepdf'); // This is the field where is the input type="file", we only accept 1 image

app.use(upload);

app.listen(PORT, ()=>{
    console.log(`Server is running at PORT: ${PORT}`);
})
