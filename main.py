import streamlit as st
from services.auth.login import render_login_page
from services.state.session_default import initial_session_state
from services.config.workout_config import EXERCISES


def main():
    st.set_page_config(
        page_title="AI Gym Assistant",
        page_icon="", 
        layout="wide",
        initial_sidebar_state="expanded")

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
            st.selectbox(
                "Exercise",options=EXERCISES, key="plan_exercise")
            st.number_input("Sets", min_value=1, max_value=10, value=3, step=1, key="plan_sets")
            st.number_input("Reps per Set", min_value=1, max_value=50, value=10, step=1, key="plan_reps")
            st.markdown("")
            start_workout =st.button("Start Workout",width="stretch",key="start_workout")
            if start_workout:
                st.session_state.workout_started = True
                st.success("Workout started!")
                st.rerun()
        else:
            st.markdown("### Workout in Progress")
            exercise = st.session_state.plan_exercise
            sets = st.session_state.plan_sets
            reps = st.session_state.plan_reps
            st.info(f"**{exercise}** -- {sets}-sets | {reps} reps")
            stop_workout = st.button("Stop Workout", width="stretch", key="stop_workout")
            if stop_workout:
                st.session_state.workout_started = False
                st.success("Workout stopped.")
                st.rerun()

            if workout_started:
                st.divider()
                st.header("Workout Status")
                exercise = st.session_state.plan_exercise
                total_reps = st.session_state.reps
                current_sets_raps = st.session_state.current_set_reps
                reps_per_set = st.session_state.plan_reps
                sets_completed = st.session_state.sets_completed
                target_sets = st.session_state.plan_sets


                st.metric("total reps", f"{total_reps}")
                st.metric("current set reps", f"{current_sets_raps}/{reps_per_set}")
                st.metric("sets completed", f"{sets_completed}/{target_sets}")

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

                if exercise == "Biceps Curls":
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

                

if __name__ == "__main__":
    main()