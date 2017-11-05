;; Auto-generated. Do not edit!


(when (boundp 'led_driver::LightDriver)
  (if (not (find-package "LED_DRIVER"))
    (make-package "LED_DRIVER"))
  (shadow 'LightDriver (find-package "LED_DRIVER")))
(unless (find-package "LED_DRIVER::LIGHTDRIVER")
  (make-package "LED_DRIVER::LIGHTDRIVER"))

(in-package "ROS")
;;//! \htmlinclude LightDriver.msg.html


(defclass led_driver::LightDriver
  :super ros::object
  :slots (_op _image ))

(defmethod led_driver::LightDriver
  (:init
   (&key
    ((:op __op) "")
    ((:image __image) (make-array 0 :initial-element 0 :element-type :integer))
    )
   (send-super :init)
   (setq _op (string __op))
   (setq _image __image)
   self)
  (:op
   (&optional __op)
   (if __op (setq _op __op)) _op)
  (:image
   (&optional __image)
   (if __image (setq _image __image)) _image)
  (:serialization-length
   ()
   (+
    ;; string _op
    4 (length _op)
    ;; uint32[] _image
    (* 4    (length _image)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _op
       (write-long (length _op) s) (princ _op s)
     ;; uint32[] _image
     (write-long (length _image) s)
     (dotimes (i (length _image))
       (write-long (elt _image i) s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _op
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _op (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; uint32[] _image
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _image (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _image i) (sys::peek buf ptr- :integer)) (incf ptr- 4)
     ))
   ;;
   self)
  )

(setf (get led_driver::LightDriver :md5sum-) "94104f9d0ed4c5d119270c5f8f23d22b")
(setf (get led_driver::LightDriver :datatype-) "led_driver/LightDriver")
(setf (get led_driver::LightDriver :definition-)
      "string op
uint32[] image

")



(provide :led_driver/LightDriver "94104f9d0ed4c5d119270c5f8f23d22b")


