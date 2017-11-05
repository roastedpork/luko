
(cl:in-package :asdf)

(defsystem "led_driver-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "LightDriver" :depends-on ("_package_LightDriver"))
    (:file "_package_LightDriver" :depends-on ("_package"))
  ))