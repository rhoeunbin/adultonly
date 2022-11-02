var i = 0;
var images = [];
var slideTime = 3000; // 3 seconds

images[0] = '../../../static/images/index/1.jpg';
images[1] = '../../../static/images/index/2.jpg';
images[2] = '../../../static/images/index/3.png';
images[3] = '../../../static/images/index/4.jpg';
images[4] = '../../../static/images/index/5.jpg';

function changePicture() {
    // document.body.style.backgroundImage = ;
    document.body.style.height = "auto";
    document.body.style.backgroundImage = "url(" + images[i] + ")";
    document.body.style.backgroundSize = "cover";
    document.body.style.backgroundRepeat = "no-repeat";
    document.body.style.overflow = "hidden";
    if (i < images.length - 1) {
        i++;
    } else {
        i = 0;
    }
    setTimeout(changePicture, slideTime);
}

window.onload = changePicture;