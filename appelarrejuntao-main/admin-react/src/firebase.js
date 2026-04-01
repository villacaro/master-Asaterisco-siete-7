// src/firebase.js  –  Firebase config for El Arrejuntao Admin
import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey:            "AIzaSyBiWv7Zrn0UUoqTm-oq_84761SvOzEBAM0",
  authDomain:        "app-el-arrejuntao.firebaseapp.com",
  projectId:         "app-el-arrejuntao",
  storageBucket:     "app-el-arrejuntao.firebasestorage.app",
  messagingSenderId: "578381240300",
  appId:             "1:578381240300:web:b205652b686be2516e92c9",
  measurementId:     "G-DEDS7SNVTX"
};

export const app  = initializeApp(firebaseConfig);
export const db   = getFirestore(app);
export const auth = getAuth(app);
