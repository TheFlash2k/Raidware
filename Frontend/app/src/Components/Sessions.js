import { useState, useEffect } from "react";
import rd01 from './resources/rd-01 1.png';
import rd02 from './resources/rd-01 inverted 1.png';
import axios from "axios";
import './styles/Sessions.css';
import Terminal, { TerminalOutput } from 'react-terminal-ui';

export default function Sessions() {

		const [sessions, setSessions] = useState([]);

		const setup_terminal = () => {
			const _rtl = document.getElementsByClassName('react-terminal-line');
			const wrapper = document.getElementsByClassName('react-terminal-wrapper');
			const cmd = document.getElementsByClassName('cmd');
			const _terminal = document.getElementsByClassName('react-terminal');

			if(_terminal !== null) {
				console.log("_Terminal: " + _terminal.length);
				console.log(_terminal)
				for(let i = 0; i < _terminal.length; i++) {
					const obj = _terminal.item(i);
					obj.style.background = '#000000';
				}
			}


			if(cmd !== null) {
				for(let i = 0; i < cmd.length; i++) {
					const obj = cmd.item(i);
					obj.style.fontSize = '15px';
				}
					// if(obj !== null) {
					// 	obj.style.overflow = 'hidden';
					// }
			}

			if(wrapper !== null) {
				for(let i = 0; i < wrapper.length; i++) {
					const obj = wrapper.item(i);
					obj.style.background = '#000000';
					obj.style.padding = '5px';
				}
					// obj.style.overflow = 'visible';
			}

			if(_rtl !== null) {
				for(let i = 0; i < _rtl.length; i++) {
					const obj = _rtl.item(i);
					obj.style.fontSize = '15px';
				}
			}
				

			const buttons = document.getElementsByClassName('react-terminal-window-buttons');
			for(let i = 0; i < buttons.length; i++) {
				const _button = buttons.item(i);
				if(_button !== null) {
					_button.style.display = 'none';
				}
			}
		}

		useEffect(() => {

			const _rtl = document.getElementsByClassName('cmd');
			if(_rtl !== null) {
				for(let i = 0; i < _rtl.length; i++) {
					console.log("Current", i)
					var obj = _rtl.item(i);
					console.log(obj)
					if(obj !== null) {
						obj.style.fontSize = '15px';
					}
				}
			}

				const url = localStorage.getItem('url') + "/sessions";

				axios.get(url, {
						headers: {
								'Authorization': 'Bearer ' + localStorage.getItem('token')
						}
				}).then((response) => {
						setSessions(response.data.sessions);
						console.log(response.data);
				}).catch((error) => {
						console.log(error);
				});
		}, []);

		const handleDark = () => {
				const div1 = document.getElementById("div1");
				const div2 = document.getElementById("div2");
				const div3 = document.getElementById("div3");
				const div4 = document.getElementById("div4");
		
				 
				if (div3.classList.contains("show")) {
						div3.classList.remove("show");
						div3.classList.add("hide");
						div4.classList.remove("hide");
						div4.classList.add("show");
					}
				 else {
						div3.classList.remove("hide");
						div3.classList.add("show");
						div4.classList.remove("show");
						div4.classList.add("hide");
					}
		
		
				if (div1.classList.contains("visible")) {
						div1.classList.remove("visible");
						div1.classList.add("hidden");
						div2.classList.remove("hidden");
						div2.classList.add("visible");
					} else {
						div1.classList.remove("hidden");
						div1.classList.add("visible");
						div2.classList.remove("visible");
						div2.classList.add("hidden");
					}
		
					
				}
		
				const handleNav = () => {
		
						const navbar = document.getElementById("navbar");
						navbar.classList.toggle("stretched");
						if (navbar.classList.contains("stretched")) {
								const mySection = document.getElementById('mySection');
								mySection.style.left = '15px'
						}
						else {
								const mySection = document.getElementById('mySection');
								mySection.style.left = '120px'
						}

				}
		
				const handleChangeDark = () => {
						const body = document.body;
						body.classList.toggle("dark-mode");
				}

				const handleTerminal = (uid) => {
						const cmd = document.getElementsByClassName('cmd');

						for(let i = 0; i < cmd.length; i++) {
							cmd[i].style.display = 'block';
						}
						const dummy = "dummy" + uid;
						const close = "closeTerminal" + uid;
						const stretch = document.getElementById(dummy);
						const terminal = document.getElementById(uid);

						const closeTerminal = document.getElementById(close);
						terminal.style.display = 'none';
						stretch.style.height = '350px';
						closeTerminal.style.display = 'block';

						setup_terminal();
				}

				const handleCloseTerminal = (uid) => {
						const dummy = "dummy" + uid;
						const close = "closeTerminal" + uid;
						const stretch = document.getElementById(dummy);
						const terminal = document.getElementById(uid);
						const closeTerminal = document.getElementById(close);

						terminal.style.display = 'block';
						stretch.style.height = '50px';
						closeTerminal.style.display = 'none';
				}

				const handleMultipleTerminal = (uid, msg) => {
					const terminal = document.getElementById("cmd_" + uid);
					terminal.textContent += msg + "\n\n";
				}

				const handlecmd = (uid, cmd) => {         
					const terminal = document.getElementById("cmd_" + uid);
					terminal.style = 'display: flex';
					
					terminal.textContent += "$ " + cmd + "\n";
					terminal.textContent += "[+] Tasked agent ";
					terminal.textContent += uid + " to run command \"" + cmd + "\"\n";
					terminal.textContent += "[+] Waiting for response...\n";
					const url = localStorage.getItem('url') + "/interact"; ;

						const data = {
							'SID': uid,
							'payload': cmd,
							'mode': 'shell'
					}

					axios.post(url, data, {
						headers: {
								'Authorization': 'Bearer ' + localStorage.getItem('token')
						}
				}).then((response) => {
						handleMultipleTerminal(uid, response.data.msg);

				}).catch((error) => {
						console.log("Error: ", error)
						console.log(error);
				});
				}



		return(
			 <div>
						<div class="toggle-container">
				<input onClick={handleDark} onChange={handleChangeDark} type="checkbox" id="toggle" class="toggle-checkbox" />
				<label for="toggle" class="toggle-label">
					<span class="toggle-inner"><i class="fa-solid fa-sun"></i></span>
					<span class="toggle-switch"><i class="fa-solid fa-moon"></i></span>
				</label>
			</div>
			<div class="logo-light show" id="div3">
				<img src={rd01} alt="LOGO" />
			</div>
			<div class="logo-dark hide" id="div4">
				<img src={rd02} alt="LOGO" />
			</div>
			<div class="Agents">
				<div class="container">
					<div class="navbar" id="navbar">
						<div class="navbar-logo-light visible" id="div1">
							<img src={rd01} alt="LOGO" />
						</div>
						<div class="navbar-logo-dark hidden" id="div2">
							<img src={rd02} alt="LOGO" />
						</div>
						<button onClick={handleNav} id="stretchButton" class="stretch-button">
							<span class="arrow-icon"></span>
						</button>
						<div class="a-tags">
              <a href="/"><i class="fa-solid fa-chart-line"></i>&nbsp; &nbsp;Dashboard</a>
              <a href="/listeners"><i class="fa-solid fa-headphones"></i> &nbsp; &nbsp;Listeners</a>
							<a href="/sessions"><i class="fa-solid fa-briefcase"></i> &nbsp; &nbsp; Session</a>
							<a href="/agents"><i class="fa-solid fa-users"></i> &nbsp; &nbsp; Agents</a>
							<a href="/loot"><i class="fa-solid fa-coins"></i> &nbsp; &nbsp; Loot</a>
							<a href="/users"><i class="fa-solid fa-user"></i> &nbsp; &nbsp; Users</a>
							<a href="/logout" className="logout"><i className="fa-solid fa-right-from-bracket"></i> &nbsp; &nbsp; Log-out</a>
          </div>
					</div>
					<div class="content" id="content">
						<div class="agent">
							<h2 class="heading" id="mySection">Sessions</h2>
						</div>
						<div class="agent-menu">
							<div class="id agent-menu-child">ID &nbsp;<i class="fa-solid fa-up-down"></i></div>
							<div class="protocol agent-menu-child">Protocol &nbsp;<i class="fa-solid fa-up-down"></i></div>
							<div class="process agent-menu-child">Process &nbsp;<i class="fa-solid fa-up-down"></i></div>
							<div class="process-id agent-menu-child">Process ID &nbsp;<i class="fa-solid fa-up-down"></i></div>
							<div class="listner agent-menu-child">OS &nbsp;<i class="fa-solid fa-up-down"></i></div>
							<div class="os agent-menu-child">Listener &nbsp;<i class="fa-solid fa-up-down"></i></div>
							<div class="pwd agent-menu-child">User &nbsp;<i class="fa-solid fa-up-down"></i></div>
							<div class="pwd agent-menu-child">PWD &nbsp;<i class="fa-solid fa-up-down"></i></div>
							<div class="pwd agent-menu-child">IP &nbsp;<i class="fa-solid fa-up-down"></i></div>
							<div class="operations agent-menu-child">Operations</div>
						</div>
						<div class="agent-items">
							<div class="agent-items-scroll">
								{ sessions.map((session) => (
								<div class="dummy dummy1" id={`dummy` + session.UID} key={session.UID}>
									<div class="dummy-stretch1 dummy-stretch">
									<div class="dummy-child dummy-child1">{session.UID}</div>
									<div class="dummy-child dummy-child1">{session.Protocol}</div>
									<div class="dummy-child dummy-child1">{session.proc}</div>
									<div class="dummy-child dummy-child1">{session.pid}</div>
									{ session.OS.toLowerCase().includes('windows') || session.OS.toLowerCase().includes('microsoft') ? (<div class="dummy-child dummy-child1 os-icons"><i class="fa-brands fa-windows fa-2x"></i></div>) : (null)}
									{ session.OS.toLowerCase().includes('mac') ? (<div class="dummy-child dummy-child1 os-icons"><i class="fa-brands fa-apple fa-2x"></i></div>) : (null)}
									{ session.OS.toLowerCase().includes('linux') || session.OS.toLowerCase().includes('ubuntu') ? (<div class="dummy-child dummy-child1 os-icons"><i class="fa-brands fa-linux fa-2x"></i></div>) : (null)}

									<div class="dummy-child dummy-child1">{session.Listener_Name}</div>
									<div class="dummy-child dummy-child1">{session.user}</div>
									<div class="dummy-child dummy-child1">{session.pwd}</div>
									<div class="dummy-child dummy-child1">{session.ip}</div>
									<div class="dummy-child dummy-child1 icons-dummy i-d">
										<div class="terminal-dummy dummy-icon">
											<i onClick={e => handleTerminal(session.UID)}  class="fa-solid fa-terminal" id={session.UID}></i>
											<i onClick={e => handleCloseTerminal(session.UID)} class="fa-solid fa-circle-xmark fa-2x"  id={"closeTerminal" + session.UID}></i>
										</div>
										<div class="download-dummy dummy-icon">
											<i class="fa-solid fa-download"></i>
										</div>
										<div class="upload-dummy dummy-icon">
											<i class="fa-solid fa-upload"></i>
										</div>
										<div class="delete-dummy dummy-icon">
											<i class="fa-solid fa-trash"></i>
										</div>
										<div class="bars-dummy dummy-icon">
											<i class="fa-solid fa-bars"></i>
										</div>
									</div>
								</div>
								<div className="cmd">
										<div>
											<Terminal 
												startState="maximised"
												hideTopBar={true}
												height="250px"
												onInput={ TerminalInput => handlecmd(session.UID, TerminalInput) }
											>
												<TerminalOutput>
													<div id={"cmd_" + session.UID}></div>
												</TerminalOutput>
											</Terminal>
										</div>
									</div>
								</div>
								))}
								</div>
							</div>
							</div>
						</div>
					</div>
				</div>
		)
}