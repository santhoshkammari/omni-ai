class ModelSettings:
    def __init__(self):
        self.state_manager = StateManager()

    def render(self):
        with st.sidebar:
            st.title("Model Settings")

            selected_model = st.selectbox(
                "Model",
                options=self.state_manager.get_state("config").AVAILABLE_MODELS,
                index=0
            )

            if selected_model != self.state_manager.get_state("selected_model"):
                self.state_manager.set_state("selected_model", selected_model)

            self._render_model_parameters()

    def _render_model_parameters(self):
        params = self.state_manager.get_state("model_params")

        new_temp = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=params.get("temperature", 0.7)
        )

        if new_temp != params.get("temperature"):
            self.state_manager.update_model_params({"temperature": new_temp})