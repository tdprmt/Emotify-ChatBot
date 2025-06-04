import streamlit as st
from transformers import pipeline
import random
import matplotlib.pyplot as plt # Untuk visualisasi riwayat emosi
from collections import Counter # Untuk menghitung frekuensi emosi

# Konfigurasi halaman
st.set_page_config(page_title="Emotify Advanced", page_icon="🚀", layout="wide")

# --- Inisialisasi Session State ---
if 'emotion_history' not in st.session_state:
    st.session_state.emotion_history = [] # Menyimpan dict {'emotion': emotion, 'confidence': confidence, 'text': user_input[:50]}
if 'user_feedback' not in st.session_state:
    st.session_state.user_feedback = []
if 'challenges' not in st.session_state:
    st.session_state.challenges = {
        "Tulis 3 hal yang kamu syukuri hari ini.": False,
        "Lakukan 10 menit peregangan atau meditasi.": False,
        "Hubungi teman atau keluarga yang lama tidak kamu sapa.": False,
        "Luangkan waktu untuk hobimu hari ini.": False,
        "Bantu seseorang tanpa mengharapkan imbalan.": False,
    }
if 'freewrite_mode' not in st.session_state:
    st.session_state.freewrite_mode = False
if 'freewrite_text' not in st.session_state:
    st.session_state.freewrite_text = ""
if 'show_freewrite_analysis_button' not in st.session_state:
    st.session_state.show_freewrite_analysis_button = False


# Muat model
@st.cache_resource
def load_emotion_model():
    """Memuat model klasifikasi teks untuk emosi."""
    return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)

classifier = load_emotion_model()

# --- Fungsi Bantuan ---
def get_emotion_response(emotion, user_input_text):
    """Menghasilkan respons Emotify berdasarkan emosi yang terdeteksi atau kata kunci, dengan variasi."""
    emotion_responses = {
        "joy": [
            "Senang sekali mendengarnya! Terus sebarkan energi positifmu! Apa satu hal lagi yang bikin kamu bahagia hari ini? 😊",
            "Luar biasa! Kebahagiaanmu menular! Ingat momen ini ya. ✨",
            "Ikut senang untukmu! Rayakan pencapaian kecil yang membawa kebahagiaan ini. 🎉"
        ],
        "sadness": [
            "Tidak apa-apa merasa sedih. Izinkan dirimu merasakannya. Emotify ada di sini menemanimu. Pelan-pelan saja, ya. 🌧️",
            "Aku mengerti ini berat. Ingat, kamu tidak sendirian. Coba tarik napas dalam, dan fokus pada satu hal kecil yang bisa membuatmu sedikit lebih baik. 🫂",
            "Kesedihan itu bagian dari hidup. Apa yang bisa Emotify bantu agar kamu merasa sedikit lebih ringan? Mungkin menuliskan perasaanmu bisa membantu? 📝"
        ],
        "anger": [
            "Marah itu energi yang perlu disalurkan dengan tepat. Coba tarik napas 5 kali. Apa yang memicu kemarahanmu? 🔥",
            "Energi marah itu kuat! Daripada merusak, coba gunakan untuk melakukan sesuatu yang produktif atau olahraga. 💪",
            "Wajar merasa marah. Penting untuk menemukan cara sehat mengungkapkannya. Hindari kata-kata yang menyakitkan, ya. 🌬️"
        ],
        "fear": [
            "Takut itu sinyal tubuh kita. Apa yang membuatmu merasa tidak aman? Mari kita hadapi bersama, satu langkah kecil saja. 🤝",
            "Rasa takut itu manusiawi. Ingatlah keberanianmu sebelumnya. Kamu lebih kuat dari yang kamu kira. 🛡️",
            "Saat takut, coba fokus pada pernapasanmu. Apa hal paling buruk yang *realistis* bisa terjadi? Dan apa yang bisa kamu lakukan? 🚶"
        ],
        "surprise": [
            "Wow, kejutan! Semoga ini kejutan yang menyenangkan ya! Bagaimana perasaanmu sekarang? 🎉",
            "Hidup penuh kejutan! Apa pelajaran atau hal menarik yang kamu dapat dari ini? 😮",
            "Kejutan bisa mengubah hari! Nikmati momen tak terduga ini. ✨"
        ],
        "disgust": [
            "Rasa tidak nyaman itu valid. Jauhi apa yang membuatmu merasa jijik jika memungkinkan. Dengarkan intuisimu. 💆‍♀️",
            "Tidak semua hal harus kita sukai. Apa yang bisa kamu lakukan untuk menciptakan lingkungan yang lebih nyaman untukmu? 🌿"
        ],
        "neutral": [
            "Netral itu juga sebuah rasa. Mungkin ini saat yang baik untuk refleksi atau sekadar menikmati ketenangan. Ada yang ingin kamu syukuri hari ini? ✨",
            "Kadang, tidak merasakan emosi kuat itu juga oke. Bagaimana kamu ingin memanfaatkan momen tenang ini? 🧘"
        ]
    }
    keyword_responses = {
        "benci": "Perasaan benci bisa sangat menguras energi. Coba pahami sumbernya. Ada baiknya bicara dengan orang dewasa yang kamu percaya. 🫂",
        "capek": "Istirahat itu hakmu, lho. Tubuh dan pikiranmu butuh di-charge. Apa hal kecil yang bisa bikin kamu rileks sekarang? 💆",
        "sendiri": "Merasa sendiri itu berat, tapi ingat, banyak yang peduli padamu. Coba hubungi teman atau keluarga, atau lakukan kegiatan yang kamu sukai. 🤗",
        "bingung": "Bingung itu tanda kamu sedang memproses banyak hal. Coba pecah masalahnya jadi bagian-bagian kecil. Satu langkah kecil sudah kemajuan! ✨",
        "kesepian": "Kesepian itu menyelinap. Coba cari koneksi, sekecil apapun. Mungkin dengan hewan peliharaan, buku, atau musik favoritmu? 💖",
        "stres": "Stres itu respons alami, tapi perlu dikelola. Coba teknik relaksasi sederhana seperti pernapasan atau jalan kaki singkat. Apa yang biasanya membantumu lebih tenang? 🧘",
        "cemas": "Cemas sering datang dengan pikiran 'gimana kalau...'. Coba fokus pada apa yang bisa kamu kontrol saat ini. Satu hal saja. Kamu kuat! 💪",
        "kecewa": "Kecewa itu wajar saat harapan tak sesuai kenyataan. Beri dirimu waktu untuk merasakannya. Apa pelajaran yang bisa diambil dari sini? 🤔",
        "galau": "Galau itu manusiawi kok, apalagi buat remaja. Coba ceritakan apa yang bikin kamu galau ke orang yang kamu percaya, atau tulis di jurnal. Kadang itu bisa membantu melihatnya lebih jelas. 💭"
    }
    possible_responses = emotion_responses.get(emotion)
    if isinstance(possible_responses, list):
        response = random.choice(possible_responses)
    else:
        response = possible_responses # This could be None if emotion not in emotion_responses
    
    if not response: 
        for key, msg in keyword_responses.items():
            if key in user_input_text.lower():
                response = msg
                break 
    if not response:
        response = "Terima kasih sudah berbagi. Emosi kamu valid dan penting untuk dikenali. Ingat, selalu ada cara untuk memahami dan mengelola perasaanmu. 🧠"
    return response

def display_emotion_chart():
    """Menampilkan grafik batang frekuensi emosi dari riwayat sesi."""
    if st.session_state.emotion_history:
        emotions = [entry['emotion'] for entry in st.session_state.emotion_history]
        emotion_counts = Counter(emotions)
        
        if emotion_counts:
            labels, values = zip(*emotion_counts.items())
            
            fig, ax = plt.subplots(figsize=(8, 4)) # Ukuran disesuaikan agar tidak terlalu besar di sidebar
            ax.bar(labels, values, color=['skyblue', 'lightcoral', 'lightgreen', 'gold', 'plum', 'lightpink', 'lightgray'])
            ax.set_ylabel('Frekuensi')
            ax.set_title('Peta Emosimu Sesi Ini')
            plt.xticks(rotation=45, ha="right") # Rotasi label agar mudah dibaca
            plt.tight_layout() # Menyesuaikan layout agar tidak terpotong
            st.pyplot(fig)
        else:
            st.write("Belum ada emosi yang cukup untuk ditampilkan di grafik.") # Should not happen if emotion_history is not empty and emotion_counts is derived
    else:
        st.write("Riwayat emosi masih kosong.")

def analyze_and_display_emotion(text_to_analyze, source="user_input"):
    """Menganalisis teks dan menampilkan hasil emosi."""
    with st.spinner("Emotify sedang memproses... 🤔"):
        try:
            output = classifier(text_to_analyze)
            # Assuming output is like [[{'label': 'joy', 'score': 0.9}]]
            if output and output[0]:
                result = output[0][0] 
                emotion = result["label"].lower()
                confidence = round(result["score"] * 100, 2)

                # Hanya tambahkan ke riwayat jika bukan dari analisis curhatan yang sudah ada
                if source == "user_input" or source == "freewrite_analysis":
                    st.session_state.emotion_history.append({
                        'emotion': emotion, 
                        'confidence': confidence, 
                        'text': text_to_analyze[:50] # Simpan 50 karakter pertama
                    })
                
                with st.chat_message("assistant", avatar="🤖"):
                    st.write(f"Emotify mengenali emosi dari '{text_to_analyze[:30]}...' sebagai **{emotion.capitalize()}** (keyakinan: {confidence}%)")
                
                emotify_response = get_emotion_response(emotion, text_to_analyze)
                with st.chat_message("assistant", avatar="💬"):
                    st.write(emotify_response)
            else:
                st.error("Tidak dapat mendeteksi emosi. Model mungkin tidak memberikan output yang diharapkan.")

        except Exception as e:
            st.error(f"Oops, ada sedikit kendala teknis: {e}")
            st.warning("Model yang digunakan berbasis Bahasa Inggris. Hasil mungkin lebih optimal jika kamu mencoba menyampaikan perasaan dalam Bahasa Inggris, atau gunakan kalimat Bahasa Indonesia yang sederhana dan umum.")

# --- Tampilan Utama Aplikasi ---
st.title("🚀 Emotify Advanced")
st.markdown("#### Chatbot edukatif yang lebih canggih untuk literasi emosi remaja!")

# Tombol untuk Mode Curhat Bebas
if st.session_state.freewrite_mode:
    if st.button("💬 Kembali ke Mode Chat Emosi", key="toggle_chat_mode"):
        st.session_state.freewrite_mode = False
        st.session_state.show_freewrite_analysis_button = bool(st.session_state.freewrite_text.strip())
        st.rerun()
else:
    if st.button("✍️ Mode Curhat Bebas (Journaling)", key="toggle_journal_mode"):
        st.session_state.freewrite_mode = True
        st.rerun()


st.markdown("---")

if st.session_state.freewrite_mode:
    st.subheader("📝 Ruang Curhat Bebasmu")
    st.markdown("Tuliskan apapun yang kamu rasakan atau pikirkan di sini. Tidak akan langsung dianalisis.")
    st.session_state.freewrite_text = st.text_area("Curahan hatimu...", value=st.session_state.freewrite_text, height=200, key="freewrite_input")
    if st.session_state.freewrite_text.strip(): # Check if text area has content
        st.session_state.show_freewrite_analysis_button = True
    # else: # if text area is empty, ensure button is hidden
        # st.session_state.show_freewrite_analysis_button = False # This might be too aggressive if user deletes text then retypes


if not st.session_state.freewrite_mode:
    st.subheader("💬 Bagikan Perasaanmu dengan Emotify")
    user_input = st.text_input("Tulis perasaanmu di sini:", placeholder="Contoh: Aku senang banget hari ini!", key="user_input_emotify_advanced")
    if user_input:
        analyze_and_display_emotion(user_input, source="user_input")
    
    # Tombol untuk menganalisis curhatan jika ada teks dan tombolnya harus muncul
    if st.session_state.show_freewrite_analysis_button and st.session_state.freewrite_text.strip():
        st.markdown("---")
        st.write("Kamu punya curhatan yang belum dianalisis:")
        st.caption(f"> {st.session_state.freewrite_text[:100]}...")
        if st.button("Analisis Curhatanku Sekarang", key="analyze_freewrite_now"):
            analyze_and_display_emotion(st.session_state.freewrite_text, source="freewrite_analysis")
            st.session_state.freewrite_text = "" # Kosongkan setelah dianalisis
            st.session_state.show_freewrite_analysis_button = False # Sembunyikan tombol
            st.rerun()


st.markdown("---")

# --- Sidebar untuk Fitur Tambahan ---
with st.sidebar:
    st.header("🛠️ Fitur Advanced Emotify 🛠️")

    with st.expander("📊 Peta Emosimu (Sesi Ini)", expanded=True):
        display_emotion_chart()
        # Tombol bersihkan riwayat dipindah ke sini agar lebih relevan dengan grafik
        if st.button("Bersihkan Riwayat & Grafik", key="clear_history_emotify_advanced"):
            st.session_state.emotion_history = []
            st.rerun()


    with st.expander("🎯 Tantangan Keseimbangan Emosi", expanded=False):
        st.markdown("Coba selesaikan tantangan ini untuk melatih kesadaran emosimu:")
        all_challenges_completed = True
        for challenge_text, completed_status in st.session_state.challenges.items():
            new_status = st.checkbox(challenge_text, value=completed_status, key=f"challenge_{challenge_text}")
            st.session_state.challenges[challenge_text] = new_status
            if not new_status:
                all_challenges_completed = False
        
        # Hitung tantangan yang selesai
        completed_count = sum(1 for status in st.session_state.challenges.values() if status)
        st.caption(f"{completed_count} dari {len(st.session_state.challenges)} tantangan selesai. Semangat!")
        if all_challenges_completed and len(st.session_state.challenges) > 0 :
             st.balloons()
             st.success("Selamat! Semua tantangan telah diselesaikan! 🎉")


    with st.expander("📚 Kamus Emosi", expanded=False):
        st.markdown("""
        * 😊 **Senang (Joy):** Perasaan bahagia, gembira, puas.
        * 😢 **Sedih (Sadness):** Perasaan kehilangan, kecewa, atau duka.
        * 😠 **Marah (Anger):** Respons terhadap frustrasi, ancaman, atau ketidakadilan.
        * 😨 **Takut (Fear):** Respons terhadap bahaya atau ancaman.
        * 😲 **Kaget/Terkejut (Surprise):** Respons terhadap sesuatu yang tak terduga.
        * 🤢 **Jijik (Disgust):** Perasaan tidak suka atau muak.
        * 😐 **Netral (Neutral):** Kondisi emosi yang tenang.
        """)

    with st.expander("💡 Aktivitas & Sumber Bantuan", expanded=False):
        st.markdown("""
        **Aktivitas Sederhana:**
        * Teknik Pernapasan (Box Breathing)
        * Jurnal Emosi
        * Bergerak (Olahraga ringan)
        * Musik Relaksasi
        * Bicara dengan Orang Terpercaya.

        **Sumber Informasi (Contoh - Ganti dengan Link Lokal):**
        * [Kesehatan Mental Remaja UNICEF](https://www.unicef.org/indonesia/id/kesehatan-mental-remaja)
        * [Layanan Psikologi HIMPSI](https://himpsi.or.id/)
        * *(PENTING: Tambahkan kontak layanan konseling remaja lokal/nasional yang kredibel)*
        """)
    
    with st.expander("🤔 Refleksi Minggu Ini", expanded=False):
        st.markdown("""
        _"Setiap emosi adalah pesan. Dengarkan baik-baik apa yang ingin disampaikannya padamu."_
        Apa satu pesan dari emosimu yang paling kamu perhatikan minggu ini?
        """)
        weekly_reflection = st.text_area("Refleksiku minggu ini...", height=100, key="weekly_reflection_input")
        if st.button("Simpan Refleksi", key="save_reflection"):
            if weekly_reflection:
                # Di aplikasi nyata, ini bisa disimpan ke database atau file
                st.session_state.last_reflection = weekly_reflection 
                st.success("Refleksi tersimpan!")
            else:
                st.warning("Tuliskan refleksimu terlebih dahulu.")


    with st.expander("📢 Beri Masukan untuk Emotify", expanded=False):
        feedback_text = st.text_area("Apa saranmu agar Emotify lebih baik?", height=100, key="feedback_emotify_advanced")
        if st.button("Kirim Masukan", key="submit_feedback_emotify_advanced"):
            if feedback_text:
                st.session_state.user_feedback.append(feedback_text)
                st.success("Terima kasih atas masukanmu! 😊")
                # Kosongkan field setelah submit
                # st.session_state.feedback_emotify_advanced = "" # This will cause error, text_area key is feedback_emotify_advanced
                # For text_area, you can't directly clear it this way after button press without rerun or more complex state handling
                # A simple way is to inform user and let it be, or use a form.
            else:
                st.warning("Mohon tulis masukanmu terlebih dahulu.")

    st.markdown("---")
    st.caption("Emotify Advanced v4 | Dibuat dengan ❤️, AI, & Matplotlib")
    st.caption("_Catatan: Matplotlib mungkin perlu diinstal (`pip install matplotlib`) jika belum ada._")
