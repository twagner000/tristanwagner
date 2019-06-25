import React, { Component } from "react";
import PropTypes from "prop-types";

class Form extends Component {
  static propTypes = {
    endpoint: PropTypes.string.isRequired
  };

  state = {
    name: "",
    email: "",
    message: ""
  };

  handleChange = e => {
    this.setState({ [e.target.name]: e.target.value });
  };

  handleSubmit = e => {
    e.preventDefault();
    const { user, task, start } = this.state;
    const entry = { user, task, start };
    const conf = {
      method: "post",
      body: JSON.stringify(entry),
      headers: new Headers({ "Content-Type": "application/json" })
    };
    fetch(this.props.endpoint, conf).then(response => console.log(response));
  };

  render() {
    const { user, task, start } = this.state;
    return (
      <div className="column">
        <form onSubmit={this.handleSubmit}>
          <div className="field">
            <label className="label">User</label>
            <div className="control">
              <input
                className="input"
                type="text"
                name="user"
                onChange={this.handleChange}
                value={user}
                required
              />
            </div>
          </div>
          <div className="field">
            <label className="label">Task</label>
            <div className="control">
              <input
                className="input"
                type="text"
                name="task"
                onChange={this.handleChange}
                value={task}
                required
              />
            </div>
          </div>
          <div className="field">
            <label className="label">Start</label>
            <div className="control">
              <input
                className="input"
                type="datetime-local"
                name="start"
                onChange={this.handleChange}
                value={start}
                required
              />
            </div>
          </div>
          <div className="control">
            <button type="submit" className="button is-info">
              Add entry
            </button>
          </div>
        </form>
      </div>
    );
  }
}

export default Form;