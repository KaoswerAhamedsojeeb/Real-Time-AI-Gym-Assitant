import streamlit as st
import os
import time
from services.ui.style_loader import load_css, inject_local_font, inject_webrtc_styles
from services.auth.login import render_login_page
from services.state.session_default import initial_session_state
from services.config.workout_config import EXERCISE_OPTIONS
from services.persistence.exercise_repository import init_db
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from services.vision.exercise_video_processor import VideoProcessor
from services.tracking.metrics import sync_metrics_update


def main():
    st.set_page_config(
        page_title="AI Gym Assistant",
        page_icon="", 
        layout="wide",
        initial_sidebar_state="expanded")

    # Load custom CSS
    css_file_path = os.path.join(os.getcwd(), "static", "styles.css")
    load_css(css_file_path)

    # Inject local font
    font_path = os.path.join(os.getcwd(), "static", "AdobeClean.otf")
    inject_local_font(font_path, "Adobe Clean")

    # Initialize the database
    init_db()

    if not render_login_page():
        
        return
    initial_session_state()
    workout_started = st.session_state.get("workout_started", False)
    with st.sidebar:
        st.title("AI Gym Assistant")

        if st.session_state.username:
            st.caption(f"Logged in as: {st.session_state.username}")

        st.divider()
        st.header("Workout Plan")
        if not workout_started:
            plan_exercise = st.selectbox("Exercise", options=EXERCISE_OPTIONS, key="plan_exercise")

            plan_sets = st.number_input("Sets", min_value=0, max_value=50, key="plan_sets", step=1)

            plan_reps = st.number_input("Reps per Set", min_value=0, max_value=50, key="plan_reps", step=1)
            
            st.markdown("")

            start_session_button = st.button("Start Workout", width="stretch", key="start_session_button")

            if start_session_button:
                st.session_state.exercise_type = plan_exercise
                st.session_state.target_sets = int(plan_sets)
                st.session_state.reps_per_set = int(plan_reps)
                st.session_state.reps = 0
                st.session_state.workout_started = True
                st.session_state.set_cycle_started_at = time.time()
                st.session_state.last_saved_sets_completed = 0
                st.session_state.last_notified_sets_completed = 0
                st.session_state.last_notified_workout_complete = False

                st.rerun()
        else:
            exercise = st.session_state.get("exercise_type")
            sets = st.session_state.get("target_sets")
            reps = st.session_state.get("reps_per_set")

            st.info(f"**{exercise}** -- {sets} Sets / {reps} Reps")

            end_session_button = st.button("End Workout", key="end_session_button", width="stretch")

            if end_session_button:
                st.session_state.workout_started = False
                st.rerun()

            if workout_started:
                st.divider()
                st.header("Workout Status")
                exercise = st.session_state.get("exercise_type")
                total_reps = st.session_state.get("reps")
                current_set_reps = st.session_state.get("current_set_reps")
                reps_per_set = st.session_state.get("reps_per_set")
                sets_completed = st.session_state.get("sets_completed")
                target_sets = st.session_state.get("target_sets")



                st.subheader("Progress")

                st.metric("Total Reps", f"{total_reps}")
                st.metric("Current Set Reps", f"{current_set_reps} / {reps_per_set}")
                st.metric("Sets Completed", f"{sets_completed} / {target_sets}")

                st.divider()


                if exercise == "Squats":
                    st.subheader("Squats Status")
                    st.metric("Knee Angle", f"{st.session_state.knee_angle:.2f}°")
                    st.metric("Back Angle", f"{st.session_state.back_angle:.2f}°")
                    st.metric("Depth Status", f"{st.session_state.depth_status}")
                    st.metric("Body Alignment", f"{st.session_state.body_alignment}")
                if exercise == "Push-ups":
                    st.subheader("Push-ups Status")
                    st.metric("Elbow Angle", f"{st.session_state.elbow_angle:.2f}°")
                    st.metric("Back Angle", f"{st.session_state.back_angle:.2f}°")
                    st.metric("Hip Status", f"{st.session_state.hip_status}")
                    st.metric("Shoulder Status", f"{st.session_state.shoulder_status}")

                if exercise == "Biceps Curls (Dumbbell)":
                    st.subheader("Biceps Curls Status")
                    st.metric("Elbow Angle", f"{st.session_state.elbow_angle:.2f}°")
                    st.metric("Swing Status", f"{st.session_state.swing_status}")
                    st.metric("Extension Status", f"{st.session_state.extension_status}")

                if exercise == "Shoulder Press":
                    st.subheader("Shoulder Press Status")
                    st.metric("Elbow Angle", f"{st.session_state.elbow_angle:.2f}°")
                    st.metric("Back Arch Status", f"{st.session_state.back_arch_status}")
                    st.metric("Balance Status", f"{st.session_state.balance_status}")

                if exercise == "Lunges":
                    st.subheader("Lunges Status")
                    st.metric("Front Knee Angle", f"{st.session_state.front_knee_angle:.2f}°")
                    st.metric("Torso Angle", f"{st.session_state.torso_angle:.2f}°")
                    st.metric("Depth Status", f"{st.session_state.depth_status}")
                    st.metric("Balance Status", f"{st.session_state.balance_status}")

    st.title("AI Gym Assistant")
    st.markdown("#### Welcome to the AI Gym Assistant!")       
    if not workout_started:
        st.markdown(
            """
            <div style="
                border: 10px dashed #444;
                border-radius: 0px;
                padding: 48px 32px;
                text-align: center;
                color: #888;
                margin-top: 32px;
                margin-bottom: 32px;
            ">
                <h2 style="color:#ccc; margin-bottom:8px;">👈 Set your workout plan</h2>
                <p style="font-size:1.05rem;">
                    Choose your exercise, sets and reps in the sidebar,<br>
                    then click <strong>Start Workout</strong> to activate the camera and AI coach.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        context = webrtc_streamer(
            key="exercise-analysis",
            mode=WebRtcMode.SENDRECV,
            video_processor_factory=VideoProcessor,
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={
                "video": True,
                "audio": False
            },
            async_processing=True
        )

        sync_metrics_update(context)

        if context.state.playing:
            time.sleep(0.25)
            st.rerun()

        inject_webrtc_styles()

    st.markdown("#### Workout History")
    inject_webrtc_styles()

    
if __name__ == "__main__":
    main()