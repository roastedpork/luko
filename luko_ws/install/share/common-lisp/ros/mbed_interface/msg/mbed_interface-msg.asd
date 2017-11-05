
(cl:in-package :asdf)

(defsystem "mbed_interface-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "JointAngles" :depends-on ("_package_JointAngles"))
    (:file "_package_JointAngles" :depends-on ("_package"))
  ))