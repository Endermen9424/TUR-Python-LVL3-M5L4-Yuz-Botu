import cv2


def process_image(image_path, output_path):
    # Yüzleri tespit etmek için önceden eğitilmiş bir sınıflandırıcı yükleme
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Görüntüyü yükleme
    image = cv2.imread(image_path)

    # Dedektör performansını artırmak için görüntüyü gri tonlamaya dönüştürme
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Görüntüdeki yüzleri tespit etme
    faces = cv2.CascadeClassifier.detectMultiScale(face_cascade, gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Tespit edilen her yüzün etrafındaki alanı bulanıklaştırma
    for (x, y, w, h) in faces:
        # Yüz bölgesini çıkarma
        face_region = image[y:y+h, x:x+w]

        # Bulanıklaştırma uygulama (kernel boyutu yüz boyutundan büyük olmamalı ve tek sayı olmalı)
        #blurred_face = cv2.blur(face_region, (99, 99))
        blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)

        # Yüz alanını bulanık görüntüyle değiştirme (düzeltildi: y:y+h)
        image[y:y+h, x:x+w] = blurred_face

    # İşlenmiş görüntüyü kaydetme
    cv2.imwrite(output_path, image)

if __name__ == "__main__":
    # Kodun işlevselliğini kontrol etme
    process_image("face.png", "output.png")
    process_image("face2.png", "output2.png")