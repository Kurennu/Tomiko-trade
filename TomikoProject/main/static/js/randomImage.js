const folderId = '1FjmE0hrB64SDuJB-7r1vWvZQvRHavIF9';
const API_KEY = 'AIzaSyBeuz7njhtLZPV0J6zDKchcovYZ3WF6Vgw';
const url = `https://www.googleapis.com/drive/v3/files?q='${folderId}'+in+parents&key=${API_KEY}&fields=nextPageToken,files(id,name,mimeType)`;

fetch(url)
  .then(response => response.json())
  .then(data => {
    const files = data.files.filter(file => file.mimeType.startsWith('image/'));

    if (files.length > 0) {
      const numberOfImages = 5;

      const randomFiles = [];
      while (randomFiles.length < numberOfImages) {
        const randomFile = files[Math.floor(Math.random() * files.length)];
        if (!randomFiles.includes(randomFile)) {
          randomFiles.push(randomFile);
        }
      }
      randomFiles.forEach((file, index) => {
        const imageUrl = `https://drive.google.com/thumbnail?id=${file.id}&sz=w1000`;

        if (index === 0) {
          document.querySelector('.main-image').src = imageUrl;
        }

        const thumbnail = document.querySelectorAll('.thumbnail')[index];
        if (thumbnail) {
          thumbnail.src = imageUrl;
        }
      });

    } else {
      console.error('No images found in the folder.');
    }
  })
  .catch(error => console.error('Error:', error));
